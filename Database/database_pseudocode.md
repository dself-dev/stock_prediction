TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

TABLE predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,          -- who ran the prediction
    ticker TEXT NOT NULL,              -- stock symbol (e.g., AAPL, TSLA)
    prediction_date DATE NOT NULL,     -- date prediction was made
    predicted_close REAL NOT NULL,     -- predicted stock price
    actual_close REAL,                 -- actual stock price (filled later)
    expected_change_pct REAL,          -- % change prediction
    went_up BOOLEAN,                   -- simple up/down prediction
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)

TABLE trades (
    trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,          -- who placed the trade
    prediction_id INTEGER,             -- link to the prediction that influenced it
    ticker TEXT NOT NULL,
    action TEXT CHECK(action IN ('BUY','SELL')), -- buy or sell
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    influenced_by_model BOOLEAN,       -- did the model affect this trade?
    trade_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(prediction_id) REFERENCES predictions(prediction_id)
)

CREATE TABLE ErrorLogs (
    error_id        INT PRIMARY KEY AUTO_INCREMENT,  -- Unique ID for each error
    username        VARCHAR(100),                   -- User who encountered the error
    timestamp       DATETIME DEFAULT CURRENT_TIMESTAMP, -- When the error happened
    file_or_ticker  VARCHAR(255),                   -- CSV file or stock symbol involved
    error_type      VARCHAR(100),                   -- Short label: FileNotFound, APIError, InvalidTicker
    error_message   TEXT,                           -- Full error details (e.g., Python exception message)
    resolved        BOOLEAN DEFAULT FALSE           -- For marking if issue is resolved
);


function register_user(username, password, email, phone):
    hash_pw = hash(password)
    insert into users (username, password_hash, email, phone)

function login(username, password):
    find user by username
    if hash(password) == stored password_hash:
        return user_id
    else:
        return "Invalid login"

function save_prediction(user_id, ticker, predicted_close, expected_change_pct, went_up):
    insert into predictions table with today's date
    return prediction_id

function update_prediction_with_actual(prediction_id, actual_close):
    update predictions set actual_close = actual_close where prediction_id = prediction_id

function save_trade(user_id, ticker, action, qty, price, prediction_id=None):
    insert trade into trades table with link to prediction_id (if applicable)

function get_user_history(user_id):
    return all predictions and trades for that user

    function log_error(username, file_or_ticker, error_type, error_message):
    INSERT INTO ErrorLogs (username, timestamp, file_or_ticker, error_type, error_message, resolved)
    VALUES (username, NOW(), file_or_ticker, error_type, error_message, false)

try:
    df = read_csv(csv_file)
except FileNotFoundError as e:
    log_error(current_user, csv_file, "FileNotFound", str(e))
    return None

