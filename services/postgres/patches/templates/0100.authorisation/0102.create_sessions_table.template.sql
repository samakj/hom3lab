CREATE TABLE IF NOT EXISTS {db.tables.sessions.schema}.{db.tables.sessions.name} (
    id             SERIAL PRIMARY KEY,
    user_id        INTEGER REFERENCES {db.tables.users.schema}.{db.tables.users.name}(id),
    created        TIMESTAMP NOT NULL,
    expires        TIMESTAMP NOT NULL,
    ip             TEXT NOT NULL,
    disabled       BOOLEAN DEFAULT FALSE
);