import sqlite3


def markdown_for(delevoper: str, branch: str):
    out = [f"# `{developer}.{branch}`" + "\n"]

    db = sqlite3.connect(":memory:")

    scripts = ["branch", "game", "release"]
    for script in scripts:
        for sub_script in ("tables", "data"):
            with open(f"db/{script}.{sub_script}.sql") as sql_file:
                db.executescript(sql_file.read())

    games = db.execute(f"""
        SELECT R.day, RR.name, P.name, G.name
        FROM       ReleaseBranch AS RB
        INNER JOIN Release       AS R ON RB.release  == R.rowid
        INNER JOIN Branch        AS B ON RB.branch   == B.rowid
        INNER JOIN Game          AS G ON R.game      == G.rowid
        INNER JOIN Region        AS RR ON R.region   == RR.rowid
        INNER JOIN Platform      AS P ON R.platform  == P.rowid
        INNER JOIN Developer     AS D ON B.developer == D.rowid
        WHERE D.name == '{developer}' AND B.name == '{branch}'
        """).fetchall()

    # TODO: game version & icon for matching in LumpClass table
    out.extend([
        "## Games",
        "| Release Date | Region | Platform | Title |",
        "| :----------- | :----- | :------- | :---- |",
        *[f"| {' | '.join(game)} |" for game in sorted(games)]])

    # TODO: links to pages for archives & tools (editors, compilers etc.) in docs

    # TODO: links to current GitHub Issues w/ this branch script's label

    # TODO: coverage by version / game
    # -- supported / unused / used lumps
    # -- overall %age

    # TODO: LumpClasses
    # -- group by system? (would require more info in db)
    # -- or have seperate pages explaining systems & which branches use them?

    # NOTE: LumpClass table will have some variable formats
    # -- we should break that out into other functions
    # -- infinity_ward.modern_warfare lump id
    # -- quake-based lump index
    # -- source-based lump index & version
    # -- Game Lump id ("sprp" etc.)
    # -- Titanfall Engine hex lump index & version
    # -- Apex Legends v0 lumps except for GameLump

    return "\n".join(out)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print(f"USAGE:    {sys.argv[0]} DEVELOPER_NAME BRANCH_NAME")
        sys.exit()
    developer, branch = sys.argv[1:]

    print(markdown_for(developer, branch))
