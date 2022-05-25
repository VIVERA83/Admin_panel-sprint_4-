import logging
import os
from marshmallow.schema import SchemaMeta
from dotenv import load_dotenv

from postgres_saver import PostgresSaver
from schemas import (
    FilmWorkSchema,
    GenreFilmWorkSchema,
    GenreSchema,
    PersonFilmWorkSchema,
    PersonSchema,
)
from sqlite_loader import SQLiteLoader

load_dotenv()

POSTGRES_DSN = os.environ.get("POSTGRES_DSN")
SQLITE_DB_NAME = "db/db.sqlite"

TABLE = {
    "film_work": FilmWorkSchema,
    "person": PersonSchema,
    "person_film_work": PersonFilmWorkSchema,
    "genre": GenreSchema,
    "genre_film_work": GenreFilmWorkSchema,
}


def load_from_sqlite(
    dsn_postgres: str, sql_db_path: str, tables: dict[str, SchemaMeta]
):
    sqlite_loader = SQLiteLoader(sql_db_path)
    postgres_saver = PostgresSaver(dsn_postgres)

    for table_name, schema in tables.items():
        for records in sqlite_loader.get_data(table_name):
            obj = [schema().load(data=dict(record)) for record in records]
            postgres_saver.insert(table_name, obj)
    sqlite_loader.close()
    postgres_saver.close()


if __name__ == "__main__":
    logging.info(f"{POSTGRES_DSN=}\n{SQLITE_DB_NAME=}\n{TABLE=}")
    load_from_sqlite(POSTGRES_DSN, SQLITE_DB_NAME, TABLE)
