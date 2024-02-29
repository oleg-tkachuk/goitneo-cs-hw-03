-- Creating the 'users' table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- Creating the 'status' table
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE CHECK (name IN ('new', 'in progress',
                                            'completed', 'on hold',
                                            'canceled', 'blocked',
                                            'backlog', 'in review'))
);

-- Creating the 'task' table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Adding unique statuses to the 'status' table
INSERT INTO status (name) VALUES ('new'), ('in progress'),
                                 ('completed'), ('on hold'),
                                 ('canceled'), ('blocked'),
                                 ('backlog'), ('in review');
