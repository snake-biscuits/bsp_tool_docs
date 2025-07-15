import sqlite3


def load_db(*scripts) -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    for script in scripts:
        for sub_script in ("tables", "data"):
            with open(f"db/{script}.{sub_script}.sql") as sql_file:
                db.executescript(sql_file.read())
    return db
