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

Change to the [task-1/](task/) directory by using the command:

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

- Use `localhost` as the host
- Use the credentials from the file [.env](task-1/.env) for the login.

You will see that this database was filled with fake data using the [seed.py](task-1/scripts/seed.py) script.
