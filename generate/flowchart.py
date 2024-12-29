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

    nodes = {
        (base_dev, base_branch): (0, 0)
        for base_dev, base_branch, fork_dev, fork_branch in forks}
    # TODO: place each branch in 2d space
    # -- chronological flow from left to right
    # -- need to know which branch is first (can't be a fork)

    # NOTE: chronological markers across the top would be neat
    # -- would require looking up releases
    # -- scripts = ["branch", "game", "release"]
    # -- chronology = db.execute("""
    # --     SELECT X.branch_name
    # --     FROM (
    # --         SELECT
    # --             MIN(R.day)                  AS release_day,
    # --             CONCAT(D.name, '.', B.name) AS branch_name
    # --         FROM       ReleaseBranch AS RB
    # --         INNER JOIN Release       AS  R ON R.rowid == RB.release
    # --         INNER JOIN Branch        AS  B ON B.rowid == RB.branch
    # --         INNER JOIN Developer     AS  D ON D.rowid == B.developer
    # --         INNER JOIN Engine        AS  E ON E.rowid == B.engine
    # --         WHERE E.name == 'Source'
    # --         AND R.day LIKE '%-%-%'
    # --         GROUP BY branch_name
    # --     ) AS X
    # --     ORDER BY X.release_day ASC
    # --     """).fetchall()

    styles = db.execute(f"""
        SELECT CONCAT('.', B.name, ' { background-color: #', B.colour, '; }')
        FROM Branch AS B
        INNER JOIN Engine AS E ON B.engine == E.rowid
        WHERE E.name == '{engine}'
        """).fetchall()
    styles = [x[0].replace("_", "-") for x in styles]

    site = "https://snake-biscuits.github.io/bsp_tool_docs"

    svg_lines = [
        "<svg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'>",
        "  <style>",
        "    .branch {",
        "      border-radius: 0.5rem;",
        "      color: #EEE;",
        "      display: inline-block;",
        "      outline: 1px solid #EEE;",
        "      overflow: auto;",
        "      padding-left: 0.5rem;",
        "      padding-right: 0.5rem;",
        "    }",
        "    a:visited { color: #E1E; }",
        *[f"    {style}" for style in styles],
        "  </style>",
        # TODO: <path>s connecting the branch nodes
        *[
            "  " + "\n  ".join([
                f"<foreignObject x='{x}' y='{y}' width='96' height='32'>",
                f"  <div class='branch {branch}' xmlns='http://www.w3.org/1999/xhtml'>",
                f"    <a href='{site}/branches/{dev}/{branch}/'>{dev}.{branch}</a>",
                "  </div>",
                "</foreignObject>"])
            for (dev, branch), (x, y) in nodes.items()],
        "</svg>"]

    print("\n").join(svg_lines)
