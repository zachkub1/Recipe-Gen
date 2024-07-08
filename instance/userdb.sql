CREATE TABLE user (
    id INTEGER NOT NULL,
    email VARCHAR(150),
    password VARCHAR(150),
    first_name VARCHAR(150),
    PRIMARY KEY (id),
    UNIQUE (email)
);

CREATE TABLE recipe (
    id INTEGER NOT NULL,
    content VARCHAR(10000),
    date DATETIME,
    user_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES user(id)
);
