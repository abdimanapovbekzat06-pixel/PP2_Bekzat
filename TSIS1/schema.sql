BEGIN;

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other');

ALTER TABLE contacts
    ADD COLUMN email VARCHAR(100),
    ADD COLUMN birthday DATE,
    ADD COLUMN group_id INTEGER REFERENCES groups(id),
    ADD COLUMN created_at TIMESTAMPTZ;

ALTER TABLE contacts
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE (contact_id, phone)
);

INSERT INTO phones (contact_id, phone, type)
SELECT id, phone, 'mobile'
FROM contacts;

COMMIT;