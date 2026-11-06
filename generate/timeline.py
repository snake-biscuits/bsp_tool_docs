from __future__ import annotations
from collections import defaultdict
import datetime
import re
from typing import Dict, List, Tuple

from . import utils


def generate_all():
    db = utils.load_db("branch", "game", "release")

    releases = query_releases(db)
    raw_svg = generate_poster(releases)

    with open("./timeline.svg", "w") as svg_file:
        svg_file.write("\n".join(raw_svg))


Release = Tuple[datetime.date, str, str, str, str, str]
# ^ (release, developer, branch, colour, game, platform)


def query_releases(db) -> List[Release]:
    releases = db.execute("""
        SELECT R.day, D.name, B.name, B.colour, G.name, P.name
        FROM        ReleaseBranch AS RB
        INNER JOIN  Release       AS  R ON R.rowid == RB.release
        INNER JOIN  Game          AS  G ON G.rowid ==  R.game
        INNER JOIN  Platform      AS  P ON P.rowid ==  R.platform
        INNER JOIN  Branch        AS  B ON B.rowid == RB.branch
        INNER JOIN  Developer     AS  D ON D.rowid ==  B.developer
        ORDER BY R.day ASC;
    """).fetchall()
    out = list()
    pattern = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
    for entry in releases:
        release_day, developer, branch, colour, game, platform = entry
        if release_day is None:
            continue
        if pattern.match(release_day) is not None:  # definite dates only
            date = datetime.date.fromisoformat(release_day)
            out.append((date, developer, branch, colour, game, platform))
    return sorted(out)


ReleaseDict = Dict[datetime.date, Tuple[str, str, str, str]]
# ^ {release: ("branch", "colour", game, platform)}
DeveloperDict = Dict[str, ReleaseDict]
# ^ {"developer": ...}

def group_releases(releases) -> DeveloperDict:
    developers = defaultdict(dict)
    for date, developer, branch, colour, game, platform in releases:
        developers[developer][date] = (branch, colour, game, platform)
    return developers


def y_for(date: datetime.date) -> int:
    return (date.year - 1996) * 72 + date.month * 6


def generate_poster(releases) -> List[str]:
    # assuming releases have been sorted by date
    first_year = releases[0][0].year
    last_year = releases[-1][0].year

    # TODO: assign columns programatically
    # each column should have no overlaps
    columns = {
        0: ("ion_storm",),  # left field
        1: ("ritual",),  # non-cod offshoot
        2: ("id_software",),  # left pillar
        3: ("raven",),
        4: ("infinity_ward", "respawn",),
        5: ("valve",),  # right pillar
        6: ("gearbox", "nexon", "outerlight"),  # long lived forks
        7: ("arkane", "troika", "ace_team",
            "loiste", "utoplanet", "strata"),
    }

    column_for_dev = {
        developer: index
        for index in columns
        for developer in columns[index]}

    svg_dev = list()
    svg_branch = list()

    firsts = set()
    branch_x = dict()

    # TODO: branch fork curves
    developers = group_releases(releases)
    # TODO: track branch lifespans
    for developer, release_d in developers.items():
        dates = sorted(release_d)
        first = dates[0]
        last = dates[-1]
        # x = column_for_dev[developer] * 144 + 72
        x = column_for_dev[developer] * 72 + 36
        top = y_for(first)
        height = y_for(last) - y_for(first) + 6
        # TODO: dev colour
        svg_dev.extend([
            f'<text x="{x}" y="{top-18}" text-anchor="middle">{developer}</text>',
            f'<rect x="{x-15}" y="{top-12}" rx="24" ry="18" width="36" height="{height+24}" fill="#CCC"/>'])
        x += 3
        # branch_d = group_branches(release_d)
        for release, (branch, colour, game, platform) in release_d.items():
            if (developer, branch) not in firsts:
                # TODO: branch X
                y = y_for(release) + 3
                svg_branch.extend([
                    f'<text x="{768}" y="{y}"><tspan fill="#{colour}">{developer}.{branch}</tspan></text>',
                    f'<line x1="{x}" y1="{y}" x2="{768}" y2="{y}" stroke="#{colour}" />'])
                firsts.add((developer, branch))
            y = y_for(release) + 3
            svg_branch.append(
                f'<circle cx="{x}" cy="{y}" r="3" fill="#{colour}"/>')

    # width = ...  # num_columns * column width + padding
    height = (2030 - 1996) * 72
    width = height  # PLACEHOLDER
    viewbox = f"0 0 {width} {height}"
    svg_header = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f'<svg width="{width}" height="{height}" viewBox="{viewbox}"',
        'version="1.1" id="svg1" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">'
    ]
    svg_footer = ["</svg>"]

    return [*svg_header, *svg_dev, *svg_branch, *svg_footer]
