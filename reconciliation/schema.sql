-- Expense Reconciliation Database Schema
-- Designed for multi-source transaction tracking and reconciliation

-- ============================================
-- CORE TABLES
-- ============================================

-- Data sources (credit cards, bank accounts, etc.)
CREATE TABLE IF NOT EXISTS sources (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('credit_card', 'bank_account', 'reimbursement_system', 'expense_tracking')),
    institution TEXT,
    account_last_four TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- All transactions from all sources
CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES sources(id),
    external_id TEXT,  -- ID from original source (e.g., Ramp UUID)
    transaction_date DATE NOT NULL,
    post_date DATE,  -- When it posted (may differ from transaction date)
    amount DECIMAL(12,2) NOT NULL,
    merchant_name TEXT,
    merchant_name_normalized TEXT,  -- Cleaned/normalized version
    description TEXT,
    category TEXT,
    subcategory TEXT,
    memo TEXT,
    is_credit BOOLEAN DEFAULT FALSE,  -- TRUE for payments/refunds
    raw_data TEXT,  -- Original row as JSON for debugging
    import_batch_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(source_id, external_id)
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_amount ON transactions(amount);
CREATE INDEX IF NOT EXISTS idx_transactions_merchant ON transactions(merchant_name_normalized);
CREATE INDEX IF NOT EXISTS idx_transactions_source ON transactions(source_id);

-- ============================================
-- MATCHING & RECONCILIATION TABLES
-- ============================================

-- Matches between transactions from different sources
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id_1 TEXT NOT NULL REFERENCES transactions(id),
    transaction_id_2 TEXT NOT NULL REFERENCES transactions(id),
    match_type TEXT NOT NULL CHECK (match_type IN (
        'exact',           -- Exact amount and date
        'date_fuzzy',      -- Amount matches, date within tolerance
        'amount_fuzzy',    -- Date matches, amount within tolerance
        'manual',          -- Manually matched by user
        'suggested'        -- System suggested, not confirmed
    )),
    confidence_score DECIMAL(5,2),  -- 0-100 confidence
    matched_by TEXT,  -- 'system' or user identifier
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(transaction_id_1, transaction_id_2)
);

-- Reconciliation runs (audit trail)
CREATE TABLE IF NOT EXISTS reconciliation_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_type TEXT NOT NULL,  -- 'cc_vs_expenses', 'expenses_vs_ramp', 'bank_vs_cc'
    source_id_1 TEXT REFERENCES sources(id),
    source_id_2 TEXT REFERENCES sources(id),
    date_range_start DATE,
    date_range_end DATE,
    total_source_1 INTEGER,  -- Count of transactions
    total_source_2 INTEGER,
    matched_count INTEGER,
    unmatched_source_1 INTEGER,
    unmatched_source_2 INTEGER,
    amount_source_1 DECIMAL(12,2),
    amount_source_2 DECIMAL(12,2),
    amount_matched DECIMAL(12,2),
    status TEXT DEFAULT 'completed',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Discrepancies found during reconciliation
CREATE TABLE IF NOT EXISTS discrepancies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reconciliation_run_id INTEGER REFERENCES reconciliation_runs(id),
    transaction_id TEXT REFERENCES transactions(id),
    discrepancy_type TEXT NOT NULL CHECK (discrepancy_type IN (
        'missing_in_target',     -- Exists in source but not target
        'missing_in_source',     -- Exists in target but not source
        'amount_mismatch',       -- Matched but amounts differ
        'date_mismatch',         -- Matched but dates differ significantly
        'duplicate',             -- Potential duplicate entry
        'already_reimbursed',    -- Expense was already reimbursed
        'needs_review'           -- Flagged for manual review
    )),
    severity TEXT DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    expected_value TEXT,
    actual_value TEXT,
    amount_difference DECIMAL(12,2),
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'investigating', 'resolved', 'ignored')),
    resolution TEXT,
    resolved_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- IMPORT TRACKING
-- ============================================

-- Track import batches for audit and rollback
CREATE TABLE IF NOT EXISTS import_batches (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES sources(id),
    file_path TEXT,
    file_hash TEXT,  -- SHA256 of imported file
    import_type TEXT,  -- 'pdf_statement', 'csv_export', 'api_sync'
    record_count INTEGER,
    amount_total DECIMAL(12,2),
    date_range_start DATE,
    date_range_end DATE,
    status TEXT DEFAULT 'completed',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- Unmatched transactions (potential issues)
CREATE VIEW IF NOT EXISTS v_unmatched_transactions AS
SELECT
    t.*,
    s.name as source_name,
    s.type as source_type
FROM transactions t
JOIN sources s ON t.source_id = s.id
WHERE t.id NOT IN (
    SELECT transaction_id_1 FROM matches
    UNION
    SELECT transaction_id_2 FROM matches
);

-- Transaction summary by source
CREATE VIEW IF NOT EXISTS v_source_summary AS
SELECT
    s.id,
    s.name,
    s.type,
    COUNT(t.id) as transaction_count,
    SUM(CASE WHEN t.is_credit THEN -t.amount ELSE t.amount END) as net_amount,
    MIN(t.transaction_date) as earliest_date,
    MAX(t.transaction_date) as latest_date
FROM sources s
LEFT JOIN transactions t ON s.id = t.source_id
GROUP BY s.id, s.name, s.type;

-- Monthly spending by source
CREATE VIEW IF NOT EXISTS v_monthly_by_source AS
SELECT
    s.name as source_name,
    strftime('%Y-%m', t.transaction_date) as month,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN t.is_credit THEN 0 ELSE t.amount END) as total_spend,
    SUM(CASE WHEN t.is_credit THEN t.amount ELSE 0 END) as total_credits
FROM transactions t
JOIN sources s ON t.source_id = s.id
GROUP BY s.name, strftime('%Y-%m', t.transaction_date)
ORDER BY month DESC, source_name;

-- Open discrepancies summary
CREATE VIEW IF NOT EXISTS v_open_discrepancies AS
SELECT
    d.*,
    t.merchant_name,
    t.amount,
    t.transaction_date,
    s.name as source_name
FROM discrepancies d
JOIN transactions t ON d.transaction_id = t.id
JOIN sources s ON t.source_id = s.id
WHERE d.status = 'open'
ORDER BY d.severity DESC, d.created_at DESC;

-- ============================================
-- SEED DATA
-- ============================================

-- Insert default sources
INSERT OR IGNORE INTO sources (id, name, type, institution, account_last_four, description) VALUES
    ('chase_visa_2030', 'Chase Visa', 'credit_card', 'Chase', '2030', 'Primary credit card'),
    ('amex_primary', 'American Express', 'credit_card', 'American Express', NULL, 'Amex card for large purchases'),
    ('boa_checking', 'Bank of America Checking', 'bank_account', 'Bank of America', NULL, 'Primary checking account'),
    ('ramp_reimbursements', 'Ramp Reimbursements', 'reimbursement_system', 'Ramp', NULL, 'Company reimbursement system'),
    ('expense_csv', 'Expense Tracking CSV', 'expense_tracking', NULL, NULL, 'Manual expense tracking spreadsheet');
