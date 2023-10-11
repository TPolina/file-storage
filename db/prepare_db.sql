CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content BYTEA NOT NULL,
    size BIGINT NOT NULL
);
