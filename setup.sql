DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip TEXT NOT NULL,
    page TEXT NOT NULL,
    user_agent TEXT NOT NULL,
    country TEXT NOT NULL
);

SELECT id, created, ip, page, user_agent, country FROM users
WHERE created=(SELECT MAX(created) FROM users)