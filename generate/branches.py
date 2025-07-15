import os

from . import utils


def generate_all():
    db = utils.load_db("branch", "game", "release")

    branches = db.execute("""
        SELECT D.name, B.name
        FROM Branch AS B
        INNER JOIN Developer AS D ON B.developer == D.rowid
        """).fetchall()

    for developer, branch in branches:
        filename = f"./docs/branches/{developer}/{branch}/index.md"
        os.makedirs(os.path.dirname(filename), exist_ok="True")
        with open(filename, "w") as md_file:
            md_file.write(index_md(db, developer, branch))
        # TODO: other generators
        # -- lump classes


def index_md(db, developer: str, branch: str):
    out = [f"# `{developer}.{branch}`" + "\n"]

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

    games2 = list()
    for date, region, publisher, game in games:
        if date is None:
            date = ""
        games2.append((date, region, publisher, game))

    # TODO: merge games to get a list of regions & platforms
    # -- keep first release date
    # TODO: region -> emoji (flags?)
    # TODO: platform.short -> :platform-short: emoji
    # TODO: game version & icon (emoji?) for matching in LumpClass table
    out.extend([
        "## Games",
        "| Release Date | Region | Platform | Title |",
        "| :----------- | :----- | :------- | :---- |",
        *[
            f"| {' | '.join(game)} |"
            for game in sorted(games2)]])

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
