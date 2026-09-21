"""Crea el schema epnas antes de ejecutar las migraciones de Django."""
import psycopg

from epnas_01.settings import DATABASES, DB_SCHEMA


def main():
    cfg = DATABASES["default"]
    with psycopg.connect(
        dbname=cfg["NAME"],
        user=cfg["USER"],
        password=cfg["PASSWORD"],
        host=cfg["HOST"],
        port=cfg["PORT"],
        autocommit=True,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{DB_SCHEMA}"')
    print(f"Schema '{DB_SCHEMA}' verificado correctamente.")


if __name__ == "__main__":
    main()
