CREATE DATABASE crypto_db;

CREATE TABLE crypto_prices (
    id TEXT,
    symbol TEXT,
    current_price NUMERIC,
    market_cap NUMERIC,
    total_volume NUMERIC
);
