import random
from faker import Faker
import psycopg2 as psy
from psycopg2 import sql, errors

fake = Faker()


def create_connection(dbname, user, password, host, port):
    try:
        return psy.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except psy.OperationalError as e:
        print(f"[error] Unable to connect to the database: {e}")
        return None


def insert_users(cur, num_users=10):
    try:
        for _ in range(num_users):
            fullname = fake.name()
            email = fake.email()
            cur.execute(
                sql.SQL(
                    "INSERT INTO {table} (fullname, email) VALUES (%s, %s)")
                .format(table=sql.Identifier('users')),
                [fullname, email]
            )
    except errors.UniqueViolation as e:
        print(f"[error] Unique constraint violation: {e}")
        cur.execute('ROLLBACK')
    except psy.Error as e:
        print(f"[error] Error inserting users: {e}")
        cur.execute('ROLLBACK')


def insert_tasks(cur, num_tasks=100, num_users=10, num_statuses=8):
    try:
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
    except errors.ForeignKeyViolation as e:
        print(f"[error] Foreign key violation: {e}")
        cur.execute('ROLLBACK')
    except psy.Error as e:
        print(f"[error] Error inserting tasks: {e}")
        cur.execute('ROLLBACK')


def main():
    dbname = 'task_manager'
    user = 'db_admin'
    password = 's7fC-Qc8hg-5wKm-An3x'
    host = 'postgres'
    port = '5432'

    try:
        print("[info] Connecting to the PostgreSQL database...")
        print(f"[info] Connections details: {dbname}/{user}@{host}:{port}")
        conn = create_connection(dbname, user, password, host, port)
        if conn is None:
            raise Exception("Failed to connect to the database.")
        else:
            print("[ok] Connection to the PostgreSQL database is successful.")

        cur = conn.cursor()

        print("[info] Start of seeding fake data into the database...")
        insert_users(cur)
        insert_tasks(cur)
        print("[ok] Seeding fake data into the database is done.")

        conn.commit()
        cur.close()
        conn.close()
        print("[ok] Connection to the PostgreSQL database is closed.")
    except Exception as e:
        print(f"[error] An error occurred: {e}")


if __name__ == '__main__':
    main()
