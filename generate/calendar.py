from __future__ import annotations
import calendar
from collections import defaultdict
import datetime
# import html
from typing import List

from . import utils
from . import timeline


def generate_all():
    db = utils.load_db("branch", "game", "release")

    raw_svg = generate_calendar(db, 1998, 11)
    with open("docs/img/calendar.svg", "w") as svg_file:
        svg_file.write("\n".join(raw_svg))


def generate_calendar(db, year, month) -> List[str]:
    width = 704 * 2
    height = 704
    viewbox = f"0 0 {width} {height}"
    svg_header = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f'<svg width="{width}" height="{height}" viewBox="{viewbox}"',
        'version="1.1" id="svg1" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">'
        """
        <style>
          <![CDATA[
            line {
              stroke-width: 3;
            }
            text {
              font-weight: bold;
              font: 32px sans-serif;
            }
          ]]>
        </style>
        """
        # background colour
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ABC" />']

    # weekday labels & linework
    svg_labels = list()
    svg_lines = list()
    for i in range(7):
        x = 64 + i * 96
        colour = "#A66" if i in (0, 6) else "#333"
        svg_labels.extend([
            f'<circle cx="{x}" cy="64" r="32" fill="{colour}" />'
            f'<text x="{x}" y="76" fill="#EEE" text-anchor="middle">{"SMTWTFS"[i]}</text>'])
        svg_lines.append(
            f'<line x1="{x}" y1="144" x2="{x}" y2="640" stroke="#ACE" />')

    date = datetime.date(year, month, 1)
    svg_labels.append(
            '<circle cx="1056" cy="0" r="128" fill="#ACE" />'
            f'<text x="1056" y="64" fill="#999" text-anchor="middle">{date.strftime("%b %Y")}</text>')

    releases = timeline.query_releases(db)
    colours = timeline.query_colours(db)

    month_releases = defaultdict(set)
    for date, developer, branch, game, platform in releases:
        if date.year == year and date.month == month:
            month_releases[date.day].add(colours[branch])

    cal = calendar.Calendar(6)
    weeks = cal.monthdayscalendar(year, month)

    # date dots
    svg_circles = list()
    svg_dates = list()
    for i, week in enumerate(weeks):
        y = 64 + (i + 1) * 96
        svg_lines.append(
            f'<line x1="768" y1="{y+16}" x2="{704*2-64}" y2="{y+16}" stroke="#ACE" />')
        for j, day in enumerate(week):
            x = 64 + j * 96
            r = 32 if day != 0 else 16
            colours = sorted(month_releases.get(day, {"ACE"}))
            svg_circles.append(
                f'<circle cx="{x}" cy="{y}" r="{r}" fill="#{colours[0]}" />')
            if len(colours) > 1:
                count = len(colours)
                svg_circles.extend([
                    f'<circle cx="{x+18+i*12}" cy="{y+28}" r="8" fill="#{colour}" />'
                    for i, colour in enumerate(colours[1:])])

            if day != 0:
                colour = "#EEE" if colours[0] != "ACE" else "#999"
                svg_dates.append(
                    f'<text x="{x}" y="{y+12}" fill="{colour}" text-anchor="middle">{day: 2d}</text>')

    svg_footer = ["</svg>"]

    return [
        *svg_header,
        *svg_labels,
        *svg_lines,
        *svg_circles,
        *svg_dates,
        *svg_footer]
