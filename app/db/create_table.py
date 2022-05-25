import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor
from load_data import POSTGRES_DSN
import logging

logging.basicConfig(
    level=logging.INFO,
)


def create_table(pg_connect: _connection):
    """Создание новых таблиц"""
    with open("db/movies_database.ddl") as file:
        sql = file.read()

    with pg_connect as conn, conn.cursor() as pg_cursor:
        pg_cursor: _cursor
        pg_cursor.execute(sql)
    logging.info("Таблицы созданы")


if __name__ == "__main__":
    logging.error(POSTGRES_DSN)
    pg_con: _connection = psycopg2.connect(dsn=POSTGRES_DSN)
    create_table(pg_con)
