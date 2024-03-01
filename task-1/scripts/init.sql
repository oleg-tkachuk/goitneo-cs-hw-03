-- Creating the 'users' table
CREATE TABLE users (
    id serial PRIMARY KEY,
    fullname varchar(100),
    email varchar(100) UNIQUE
);

-- Creating the 'status' table
CREATE TABLE status (
    id serial PRIMARY KEY,
    name varchar(50) UNIQUE CHECK (name IN ('new',
                                            'in progress',
                                            'completed',
                                            'on hold',
                                            'canceled',
                                            'blocked',
                                            'backlog',
                                            'in review'))
);

-- Creating the 'task' table
CREATE TABLE tasks (
    id serial PRIMARY KEY,
    title varchar(100),
    description text,
    status_id integer,
    user_id integer,
    FOREIGN KEY (status_id) REFERENCES status (id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Adding unique statuses to the 'status' table
INSERT INTO status (name)
    VALUES ('new'),
    ('in progress'),
    ('completed'),
    ('on hold'),
    ('canceled'),
    ('blocked'),
    ('backlog'),
    ('in review');

