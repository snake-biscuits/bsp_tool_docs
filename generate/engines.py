import collections

from . import utils


def generate_all():
    db = utils.load_db("branch")

    engines = db.execute("SELECT name FROM Engine").fetchall()

    with open("./docs/engines/svgs.md", "w") as outfile:
        outfile.write("# Engine `.svg`s" + "\n\n")
        for (engine,) in engines:
            outfile.write(f"## {engine}" + "\n")
            outfile.write('<div class="svg-wrapper">')
            outfile.write(forks_svg(db, engine) + "\n\n")
            outfile.write('</div>')


def forks_svg(db, engine):
    # TODO: mermaid output for debugging
    # TODO: track engine of each branch collected
    forks = db.execute(f"""
        SELECT BD.name, BB.name, FD.name, FB.name
        FROM       BranchFork AS BF
        INNER JOIN Branch     AS BB ON BB.rowid == BF.base
        INNER JOIN Developer  AS BD ON BD.rowid == BB.developer
        INNER JOIN Branch     AS FB ON FB.rowid == BF.fork
        INNER JOIN Developer  AS FD ON FD.rowid == FB.developer
        INNER JOIN Engine     AS E  ON BB.engine == E.rowid OR FB.engine == E.rowid
        WHERE E.name == '{engine}'
        """).fetchall()

    # TODO: place each branch in 2d space
    # -- chronological flow from left to right
    # -- need to know which branch is first (can't be a fork)
    nodes = dict()
    node_forks = collections.defaultdict(set)
    for base_dev, base_branch, fork_dev, fork_branch in forks:
        base = (base_dev, base_branch)
        fork = (fork_dev, fork_branch)
        if base not in nodes:  # should only happen once!
            x, y = 0, 0
            nodes[base] = (x, y)
        else:
            x, y = nodes[base]
        x += 128
        y += 24 * len(node_forks[base])
        # text_width = 8 * (len(base_dev) + 1 + len(base_branch))
        # gap = text_width + 48
        nodes[fork] = (x, y)
        node_forks[base].add(fork)

    if len(nodes) == 0:
        branches = db.execute("""
            SELECT D.name, B.name
            FROM       Branch    AS B
            INNER JOIN Developer AS D ON D.rowid == B.developer
            INNER JOIN Engine    AS E ON E.rowid == B.engine""" + f"""
            WHERE E.name == '{engine}'
            """).fetchall()
        if len(branches) == 0:
            return "<!-- engine with no branches -->"
        x, y = 0, 0
        for dev, branch in branches:
            nodes[(dev, branch)] = (x, y)
            y += 24

    # construct svg

    width = max(x for x, y in nodes.values()) + 128
    height = max(y for x, y in nodes.values()) + 24
    width = max(256, width)
    height = max(64, height)
    bounds = f"0 0 {width} {height}"

    def style_for(branch):
        return f"branch-{branch.replace('_', '-')}"

    node_links = [
        (nodes[base], nodes[fork])
        for base in node_forks
        for fork in node_forks[base]]

    site = "https://snake-biscuits.github.io/bsp_tool_docs"

    svg_lines = [
        f"<svg viewBox='{bounds}' xmlns='http://www.w3.org/2000/svg'>",
        # TODO: <path>s connecting the branch nodes
        # *[
        #     f'<path d="M {bx+80} {by+12} L {fx+12} {fy+12}"/>'
        #     for (bx, by), (fx, fy) in node_links],
        *[
            f'<path d="M {bx+96} {by+12} C {bx+120} {by+12}, {fx-12} {fy+12}, {fx+4} {fy+12}"/>'
            for (bx, by), (fx, fy) in node_links],
        *[
            "  " + "\n  ".join([
                # TODO: variable width based on text width
                f"<foreignObject x='{x}' y='{y}' width='256' height='32'>",
                f"    <a class='node {style_for(branch)}' href='{site}/branches/{dev}/{branch}/'>{dev}.{branch}</a>",
                "</foreignObject>"])
            for (dev, branch), (x, y) in nodes.items()],
        "</svg>"]

    return "\n".join(svg_lines)


if __name__ == "__main__":
    generate_all()
