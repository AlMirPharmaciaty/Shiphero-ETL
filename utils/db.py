from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects.mysql import insert as mysql_insert
from config.settings import DB_URL


def db_upsert(db: Session, model, data: list, batch_size: int = 1500):
    """Upsert data into database"""
    table = model.__table__
    primary_keys = [key.name for key in inspect(table).primary_key]
    for i in range(0, len(data), batch_size):
        if DB_URL.startswith("mysql"):
            stmt = mysql_insert(table).values(data[i:i+batch_size])
            stmt = stmt.on_duplicate_key_update(stmt.inserted)
        else:
            stmt = sqlite_insert(table).values(data[i:i+batch_size])
            stmt = stmt.on_conflict_do_update(index_elements=primary_keys,
                                              set_=stmt.excluded)
        db.execute(stmt)
