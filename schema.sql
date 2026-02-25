CREATE TABLE IF NOT EXISTS stock_data (
    date DATE,
    symbol VARCHAR,
    qty_financed INTEGER,
    amt_financed REAL,
    PRIMARY KEY (date, symbol)
);

CREATE TABLE IF NOT EXISTS daily_summary (
    date DATE PRIMARY KEY,
    total_outstanding_begin REAL,
    fresh_exposure REAL,
    exposure_liquidated REAL,
    net_outstanding_end REAL
);
