\c zywadb;

GRANT ALL PRIVILEGES ON DATABASE zywadb TO admin_user;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_user;

CREATE TABLE card_status_events (
    id SERIAL PRIMARY KEY,
    card_id VARCHAR(255),
    user_contact VARCHAR(255),
    timestamp TIMESTAMP,
    status VARCHAR(255),
    comment TEXT
);

CREATE INDEX idx_timestamp ON card_status_events(timestamp);
CREATE INDEX idx_card_id ON card_status_events(card_id);
CREATE INDEX idx_user_contact ON card_status_events(user_contact);

