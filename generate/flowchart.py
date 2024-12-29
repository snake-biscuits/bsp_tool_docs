if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(f"USAGE:    {sys.argv[0]} ENGINE_NAME")
    engine = sys.argv[1]

    # load the db
    import sqlite3
    db = sqlite3.connect(":memory:")
    scripts = ["branch"]
    for script in scripts:
        for sub_script in ("tables", "data"):
            with open(f"generate/db/{script}.{sub_script}.sql") as sql_file:
                db.executescript(sql_file.read())

    forks = db.execute(f"""
        SELECT BD.name, BB.name, FD.name, FB.name
        FROM       BranchFork AS BF
        INNER JOIN Branch     AS BB ON BB.rowid == BF.base
        INNER JOIN Developer  AS BD ON BD.rowid == BB.developer
        INNER JOIN Branch     AS FB ON FB.rowid == BF.fork
        INNER JOIN Developer  AS FD ON FD.rowid == FB.developer
        INNER JOIN Engine     AS E  ON BB.engine == E.rowid AND FB.engine == E.rowid
        WHERE E.name == '{engine}'
        """).fetchall()

    mermaid_lines = [
        "```mermaid",
        # NOTE: would do markdown links but it breaks
        # -- developer.branch["`[developer.branch](../branches/developer/branch.md)`"]
        *["{}.{} --> {}.{}".format(*fork) for fork in forks],
        "```"]

    print("\n".join(mermaid_lines))
