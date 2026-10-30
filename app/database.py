import os
from contextlib import contextmanager
import pymysql
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def conectar():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not db_user or not db_password:
        raise RuntimeError(
            "Faltan variables de entorno: DB_USER y/o DB_PASSWORD. Revisa el archivo .env"
        )

    conexion = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=db_user,
        password=db_password,
        database=os.getenv("DB_NAME", "tienda"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
        connect_timeout=10,
    )
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()