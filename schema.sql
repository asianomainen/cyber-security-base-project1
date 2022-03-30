CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN DEFAULT false
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    sent_at TIMESTAMP
);
