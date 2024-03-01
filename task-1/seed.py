import random
import psycopg2 as psy
from psycopg2 import sql
from faker import Faker


fake = Faker()


def create_connection(dbname, user, password, host, port):
    return psy.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )


def insert_users(cur, num_users=10):
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        cur.execute(
            sql.SQL("INSERT INTO {table} (fullname, email) VALUES (%s, %s)")
            .format(table=sql.Identifier('users')),
            [fullname, email]
        )


def insert_tasks(cur, num_tasks=100, num_users=10, num_statuses=8):
    for _ in range(num_tasks):
        title = fake.sentence(nb_words=6)
        description = fake.text(max_nb_chars=200)
        status_id = random.randint(1, num_statuses)
        user_id = random.randint(1, num_users)
        cur.execute(
            sql.SQL(
                "INSERT INTO {table} (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)")
            .format(table=sql.Identifier('tasks')),
            [title, description, status_id, user_id]
        )


def main():
    dbname = 'task_manager'
    user = 'db_admin'
    password = 's7fC-Qc8hg-5wKm-An3x'
    host = 'localhost'
    port = '5432'

    print('* Connecting to the PostgreSQL database...')
    print(f'* Connections details: {dbname}/{user}@{host}:{port}')
    conn = create_connection(dbname, user, password, host, port)
    cur = conn.cursor()

    print('* Start of seeding fake data into the database...')
    insert_users(cur)
    insert_tasks(cur)
    print('* Seeding fake data into the database is done.')

    conn.commit()
    cur.close()
    conn.close()
    print('* Connection to the PostgreSQL database is closed.')


if __name__ == '__main__':
    main()
