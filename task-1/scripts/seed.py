import random
import argparse
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


def validate_port(value):
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{value} is not a valid port number.")

    if 0 <= port <= 65535:
        return port
    else:
        raise argparse.ArgumentTypeError(
            f"Port number {port} is out of range. Must be 0-65535.")


def cli():
    parser = argparse.ArgumentParser(
        description='Seed database with fake data.')
    parser.add_argument('--dbname', required=True, type=str,
                        default='task_manager', help='Database name (default: %(default)s)')
    parser.add_argument('--user', required=True, type=str,
                        default='db_admin', help='Database user (default: %(default)s)')
    parser.add_argument('--password', required=True,
                        type=str, help='Database password')
    parser.add_argument('--host', required=True, type=str,
                        default='localhost', help='Database host (default: %(default)s)')
    parser.add_argument('--port', required=True, type=validate_port,
                        default=5432, help='Database port (default: %(default)s)')

    args = parser.parse_args()

    return args


def main():
    args = cli()

    try:
        print("[info] Connecting to the PostgreSQL database...")
        print(f"[info] Connections details: {args.dbname}/{args.user}@{args.host}:{args.port}")
        conn = create_connection(args.dbname, args.user, args.password, args.host, args.port)
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
