CREATE TABLE IF NOT EXISTS users
(
    id         INTEGER PRIMARY KEY,
    full_name  VARCHAR   NOT NULL,
    role       VARCHAR   NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
)