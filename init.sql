CREATE TABLE IF NOT EXISTS jobs
(
    id         UUID         NOT NULL PRIMARY KEY,
    message    TEXT         NOT NULL,
    number     INTEGER      NOT NULL,
    created_at TIMESTAMP    NOT NULL
);

CREATE TABLE IF NOT EXISTS results
(
    id         UUID         NOT NULL PRIMARY KEY,
    message    TEXT         NOT NULL,
    result     INTEGER      NOT NULL,
    created_at TIMESTAMP    NOT NULL
);
