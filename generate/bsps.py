import collections

from . import utils


def generate_all():
    db = utils.load_db("branch", "bsp")

    bsp_classes = db.execute("""
        SELECT D.name, BC.name
        FROM       BspClass  AS BC
        INNER JOIN Developer AS D ON BC.developer == D.rowid
        """).fetchall()

    for developer, bsp_class in bsp_classes:
        with open(f"./docs/bsps/{developer}/{bsp_class}.md", "w") as md_file:
            md_file.write(index_md(db, developer, bsp_class))


def index_md(db, developer: str, bsp_class: str):
    out = [f"# `{developer}.{bsp_class}`" + "\n"]

    # BspClass(es) this one is a fork of
    parent_classes = db.execute(f"""
        SELECT BD.name, B.name
        FROM BspClassFork AS BCF
        INNER JOIN BspClass  AS B  ON BCF.base == B.rowid
        INNER JOIN Developer AS BD ON B.developer == BD.rowid
        INNER JOIN BspClass  AS F  ON BCF.fork == F.rowid
        INNER JOIN Developer AS FD ON F.developer == FD.rowid
        WHERE FD.name == '{developer}' AND F.name == '{bsp_class}'
        """).fetchall()

    # NOTE: should have 0 or 1 parents
    out.extend([
        f"Fork of [`{developer}.{bsp_class}`](../{developer}/{bsp_class}.md)"
        for developer, bsp_class in parent_classes])

    if len(parent_classes) > 0:
        out.append("")  # line break

    # branches used w/ this BspClass
    branch_query = db.execute(f"""
        SELECT D.name, B.name
        FROM BspClassBranch AS BCB
        -- limit to current BspClass
        INNER JOIN BspClass  AS BC  ON BCB.bsp_class == BC.rowid
        INNER JOIN Developer AS BCD ON BC.developer == BCD.rowid
        -- developer & branch that can be used with this BspClass
        INNER JOIN Branch    AS B ON BCB.branch == B.rowid
        INNER JOIN Developer AS D ON B.developer == D.rowid
        WHERE BCD.name == '{developer}' AND BC.name == '{bsp_class}'
        """).fetchall()

    branches = collections.defaultdict(set)
    for developer, branch in branch_query:
        branches[developer].add(branch)
    assert len(branches) > 0

    out.extend([
        "",
        "## Supported Branches",
        ""])

    for developer in sorted(branches):
        out.append(f" * `{developer}`")
        for branch in sorted(branches[developer]):
            name = f"{branch}"
            link = f"../../branches/{developer}/{branch}/index.md"
            out.append(f"    - [`{name}`]({link})")

    return "\n".join(out)
