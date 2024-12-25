"""generate a .md for the given branch script"""


def markdown_for(branch_script):
    out = list()
    developer, branch = branch_script.__name__.split(".")[-2:]
    out.append(f"# `{developer}.{branch}`" + "\n")

    # TODO: load the sql db
    # TODO: table of games
    out.extend([
        "## Games",
        "| Release Date | Region | Platform | Title |",
        "| :----------- | :----- | :------- | :---- |"])
    # for game in games:
    #     row = f"| {'|'.join([game.day, game.region, game.platform, game.title])} |"
    #     out.append()
    # TODO: game version & icon for matching in LumpClass table

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
