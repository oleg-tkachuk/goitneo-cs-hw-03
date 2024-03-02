# goitneo-cs-hw-03

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

To stop and delete all resources that were created using the `docker-compose up` command in the current Docker Compose project, run the command in the [task-2/](task-2/) directory:

```shell
docker-compose down --volumes
```
