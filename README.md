# goitneo-cs-hw-03

## Task 1

## Prerequisites

0. Clone this repository to your local computer.
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install [Docker Compose](https://docs.docker.com/compose/install/)
3. Install [pgAdmin 4](https://www.pgadmin.org/download/)
4. Install Python libraries:

   ```shell
   pip3 install psycopg2-binary
   pip3 install faker
   ```

## HOWTO

Change to the [task-1/](task-1/) directory by using the command:

   ```shell
   cd task-1/
   ```

Run the following command to start the services defined in the [docker-compose.yml](task-1/docker-compose.yaml):

```shell
docker-compose up
```

Or, if you prefer to run in detached mode (in the background):

```shell
docker-compose up -d
```

Now you can connect to the PostgreSQL database using pgAdmin 4:

- Use `localhost` as the host.
- Use the credentials from the file [.env](task-1/.env) for the login.

You will see that this database was filled with fake data using the [seed.py](task-1/scripts/seed.py) script.

To stop and delete all resources that were created using the docker-compose up command in the current Docker Compose project, run the command in the [task-1/](task-1/) directory:

```shell
docker-compose down --volumes
```

## SQL queries

1 Get all tasks of a specific user:

```sql
SELECT * FROM tasks WHERE user_id = <user_id>;
```

Replace `<user_id>` with the ID of the user for whom you want to get the task.

2 Select a task by a specific status:

```sql
SELECT * FROM tasks WHERE status_id IN (SELECT id FROM status WHERE name = 'new');
```

3 Update the status of a specific task:

```sql
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = <task_id>;
```

Replace `<task_id>` with the identifier of the task whose status you want to change.

4 Get a list of users who do not have any tasks:

```sql
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);
```

5 Add a new task for a specific user:

```sql
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('<title>', '<description>', <status_id>, <user_id>);
```

Replace `<title>`, `<description>`, `<status_id>`, and `<user_id>` with the appropriate values.

6 Get all tasks that have not yet been completed:

```sql
SELECT * FROM tasks
WHERE status_id NOT IN (SELECT id FROM status WHERE name = 'completed');
```

7 Delete a specific task:

```sql
DELETE FROM tasks WHERE id = <task_id>;
```

Replace `<task_id>` with the identifier of the task you want to delete.

8 Find users with a specific email address:

```sql
SELECT * FROM users WHERE email LIKE '%<part_of_email>%';
```

Replace `<part_of_email>` with the part of the email to search for.

9 Update the username:

```sql
UPDATE users SET fullname = '<new_fullname>' WHERE id = <user_id>;
```

Replace <new_fullname> and <user_id> with the new name and user ID, respectively.

10 Get the number of tasks for each status:

```sql
SELECT status.name, COUNT(tasks.id) FROM status
LEFT JOIN tasks ON status.id = tasks.status_id
GROUP BY status.name;
```

11 Get tasks assigned to users with a specific email domain:

```sql
SELECT tasks.* FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE '%@example.com';
```

Replace `example.com` with the desired domain.

12 Get a list of tasks that have no description:

```sql
SELECT * FROM tasks WHERE description IS NULL OR description = '';
```

13 Select users and their tasks that are in the 'in progress' status.
Use INNER JOIN to get a list of users and their tasks with a specific status.

```sql
SELECT users.*, tasks.* FROM users
INNER JOIN tasks ON users.id = tasks.user_id
INNER JOIN status ON tasks.status_id = status.id
WHERE status.name = 'in progress';
```

14 Get the users and the number of their tasks.
Use LEFT JOIN and GROUP BY to select users and count their tasks:

```sql
SELECT users.fullname, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.id, users.fullname;
```

## Task 2

## Prerequisites

0. Clone this repository to your local computer.
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install [Docker Compose](https://docs.docker.com/compose/install/)
3. Install Python libraries:

   ```shell
   pip3 install pymongo
   pip3 install python-dotenv
   ```

## HOWTO

Change to the [task-2/](task-2/) directory by using the command:

   ```shell
   cd task-2/
   ```

Run the following command to start the services defined in the [docker-compose.yml](task-2/docker-compose.yaml):

```shell
docker-compose up
```

Or, if you prefer to run in detached mode (in the background):

```shell
docker-compose up -d
```

Now run the script [demo.sh](task-2/demo.sh):

```shell
./demo.sh
```

or

```shell
bash ./demo.sh
```

This demo script will show you some examples of how to use the [mongo-crud-cats.py](task-2/mongo-crud-cats.py) script.
You can also run [mongo-crud-cats.py](task-2/mongo-crud-cats.py) with the `--help` switch for more information on how to use it.

```shell
python3 ./mongo-crud-cats.py --help
```

To stop and delete all resources that were created using the docker-compose up command in the current Docker Compose project, run the command in the [task-2/](task-2/) directory:

```shell
docker-compose down --volumes
```
