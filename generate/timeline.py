from __future__ import annotations
from collections import defaultdict
import datetime
import html
import re
from typing import Dict, List, Tuple

from . import utils


def generate_all():
    db = utils.load_db("branch", "game", "release")

    releases = query_releases(db)
    colours = query_colours(db)
    forks = query_forks(db)
    raw_svg = generate_poster(releases, colours, forks)

    with open("./timeline.svg", "w") as svg_file:
        svg_file.write("\n".join(raw_svg))


Release = Tuple[datetime.date, str, str, str, str, str]
# ^ (release, developer, branch, colour, game, platform)


def query_colours(db) -> Dict[str, str]:
    colours = db.execute(
        "SELECT name, colour FROM Branch;").fetchall()
    return dict(colours)


def query_forks(db) -> Dict[str, str]:
    forks = db.execute("""
        SELECT F.name, D.name, B.name
        FROM       BranchFork AS BF
        INNER JOIN Branch     AS  B ON B.rowid == BF.base
        INNER JOIN Developer  AS  D ON D.rowid == B.developer
        INNER JOIN Branch     AS  F ON F.rowid == BF.fork
    """).fetchall()
    return {
        fork: (base_developer, base_branch)
        for fork, base_developer, base_branch in forks}


def query_releases(db) -> List[Release]:
    releases = db.execute("""
        SELECT R.day, D.name, B.name, G.name, P.name
        FROM       ReleaseBranch AS RB
        INNER JOIN Release       AS  R ON R.rowid == RB.release
        INNER JOIN Game          AS  G ON G.rowid ==  R.game
        INNER JOIN Platform      AS  P ON P.rowid ==  R.platform
        INNER JOIN Branch        AS  B ON B.rowid == RB.branch
        INNER JOIN Developer     AS  D ON D.rowid ==  B.developer
        ORDER BY R.day ASC;
    """).fetchall()
    out = list()
    pattern = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
    for entry in releases:
        release_day, developer, branch, game, platform = entry
        if release_day is None:
            continue
        if pattern.match(release_day) is not None:  # definite dates only
            date = datetime.date.fromisoformat(release_day)
            out.append((date, developer, branch, game, platform))
    return sorted(out)


ReleaseDict = Dict[datetime.date, Tuple[str, str, str]]
# ^ {release: ("branch", "game", "platform")}
DeveloperDict = Dict[str, ReleaseDict]
# ^ {"developer": ...}


def group_developers(releases) -> DeveloperDict:
    developers = defaultdict(dict)
    for date, developer, branch, game, platform in releases:
        developers[developer][date] = (branch, game, platform)
    return developers


def group_branches(releases):
    branches = defaultdict(dict)
    for date, developer, branch, game, platform in releases:
        branches[(developer, branch)][date] = (game, platform)
    return branches


def x_for(developer: str):
    # NOTE: chosen by hand, should have no overlaps
    columns = {
        0: ("ion_storm",),  # left field
        1: ("ritual",),  # non-cod offshoot
        2: ("id_software",),  # left pillar
        3: ("raven",),
        4: ("infinity_ward", "respawn",),
        5: ("valve",),  # right pillar
        6: ("gearbox", "nexon", "outerlight"),  # long lived forks
        7: ("arkane", "troika", "ace_team",
            "loiste", "utoplanet", "strata")}  # short lived forks

    column_for_dev = {
        developer: index
        for index in columns
        for developer in columns[index]}

    return 144 + column_for_dev[developer] * 72


def x_offset_for(branch: str = None):
    branch_offsets = {
        # arkane
        "dark_messiah_sp": -6,  # 2006
        "dark_messiah_mp": +6,  # 2006
        # gearbox
        "blue_shift": -6,  # 2001-2005
        "nightfire": +6,  # 2002
        # id_software
        "quake": 0,  # 1996-2021
        "quake2": -6,  # 1997-2023
        "quake3": +6,  # 1999-2020
        "quake64": -12,  # 1998-2021
        "qfusion": +12,  # 2006-2019
        "remake_quake": -18,  # 2016-2021
        "qbism": 0,  # 2023
        # infinity_ward
        # NOTE: almost no overlaps!
        "call_of_duty1_demo": 0,  # 2003
        "call_of_duty1": -6,  # 2003-2004
        "call_of_duty2": 0,  # 2005
        "modern_warfare": +6,  # 2007
        # nexon
        # NOTE: dates are a bit vague
        "cso2": -6,  # 2013
        "cso2_2018": +6,  # 2013
        "vindictus69": -6,  # 2012
        "vindictus": +6,  # 2012
        # raven
        "hexen2": 0,  # 1997
        "soldier_of_fortune": -6,  # 2000-2001
        "soldier_of_fortune2": +6,  # 2000-2020
        # respawn
        "titanfall": 0,  # 2014-2020
        "titanfall_x360": -6,  # 2014
        "titanfall2": +6,  # 2016-2020
        "apex_legends": -6,  # 2019-2021
        "apex_legends50": 0,  # 2021-2022
        "apex_legends51": +6,  # 2022-2024
        "apex_legends52": +12,  # 2024
        # ritual
        "sin": 0,  # 1998-2020
        "fakk2": -6,  # 2000
        "mohaa": +6,  # 2002-2012
        "mohaa_bt": +12,  # 2003
        "star_trek_elite_force2_demo": -6,  # 2003
        "star_trek_elite_force2": -12,  # 2003
        # valve
        "goldsrc": 0,  # 1998-2018
        "source": +6,  # 2004-2022
        # "source_xbox": +12,  # 2004?
        "orange_box": +12,  # 2006-2022
        "orange_box_x360": +18,  # 2007-2009
        "left4dead": -6,  # 2008
        "left4dead2": -12,  # 2009-2014
        "alien_swarm": -18,  # 2010-2017
        "sdk_2013": +24,  # 2011-2016
        "sdk_2013_x360": +30,  # 2011-2012
        "source_filmmaker": +18,  # 2012
    }

    return branch_offsets.get(branch, 0)


def y_for(date: datetime.date) -> int:
    return (date.year - 1995) * 72 + date.month * 6


def generate_poster(releases, colours, forks) -> List[str]:
    # assuming releases have been sorted by date
    first_year = releases[0][0].year
    last_year = releases[-1][0].year

    # date marker
    svg_years = list()
    for year in range(first_year, 2026+1):
        y = y_for(datetime.date(year, 1, 1))
        svg_years.extend([
            f'<text x="48" y="{y-4}" fill="#CCC">{year}</text>',
            f'<line x1="6" y1="{y}" x2="96" y2="{y}" stroke="#CCC" />'])
        svg_years.extend([
            f'<line x1="12" y1="{y+i*6}" x2="36" y2="{y+i*6}" stroke="#999" />'
            for i in range(1, 12)])

    # branch lines
    svg_branch = list()
    branches = group_branches(releases)
    for (developer, branch), dates_d in branches.items():
        dates = sorted(dates_d)
        first = dates[0]
        last = dates[-1]
        x = x_for(developer) + x_offset_for(branch) - 1
        top = y_for(first)
        height = y_for(last) - y_for(first) + 18
        colour = colours[branch]
        svg_branch.append(
            f'<rect x="{x}" y="{top}" rx="2" ry="2" width="3" height="{height}" fill="#{colour}"/>')

    svg_dev = list()
    for developer, release_d in group_developers(releases).items():
        # developer columns
        dates = sorted(release_d)
        first = dates[0]
        last = dates[-1]
        x = x_for(developer)
        top = y_for(first)
        height = y_for(last) - y_for(first) + 18
        # TODO: dev colour
        svg_dev.extend([
            # f'<text x="{x}" y="{top-18}" fill="#CCC" text-anchor="middle">{developer}</text>',
            f'<rect x="{x-32}" y="{top-12}" rx="20" ry="20" width="64" height="{height+24}" fill="#333"/>'])

    firsts = set()
    # TODO: branch-fork connecting lines/curves
    svg_fork = list()
    svg_release = list()
    for date, developer, branch, game, platform in releases:
        # release dots
        x = x_for(developer) + x_offset_for(branch)
        y = y_for(date)
        colour = colours[branch]
        svg_release.append(
            f'<circle cx="{x}" cy="{y}" r="3" fill="#{colour}"/>')
        if (developer, branch) not in firsts:
            firsts.add((developer, branch))
            # svg_branch.extend([
            #     # f'<text x="{768}" y="{y}" fill="#{colour}">{html.escape(game)}</text>',
            #     f'<text x="{768}" y="{y}" fill="#{colour}">{branch}</text>',
            #     f'<line x1="{x}" y1="{y}" x2="{768}" y2="{y}" stroke="#{colour}" />'])
            if branch not in forks:
                continue
            fork = branch
            base_developer, base = forks[branch]
            x1 = x_for(base_developer) + x_offset_for(base)
            x2 = x_for(developer) + x_offset_for(fork)
            y = y_for(date)
            colour = colours[fork]
            svg_fork.append(
                f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#{colour}" />')
            # TODO: second up/down line if branch line doesn't reach

    width = 768  # rough estimate
    height = (2027 - 1995) * 72
    viewbox = f"0 0 {width} {height}"
    svg_header = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f'<svg width="{width}" height="{height}" viewBox="{viewbox}"',
        'version="1.1" id="svg1" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">'
        # background colour
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#222" />'
    ]
    svg_footer = ["</svg>"]

    return [
        *svg_header,
        *svg_years,
        *svg_dev,
        *svg_fork,
        *svg_branch,
        # *svg_release,
        *svg_footer]
