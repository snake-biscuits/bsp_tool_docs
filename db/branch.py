"""bsp_tool.branches -> sql"""
import json
import sqlite3
from types import ModuleType

import common

import bsp_tool


def generate():
    """populate tables & save to .sql"""
    db = sqlite3.connect(":memory:")
    common.run_script(db, "branch.tables.sql")

    tables = list()

    tables.append("Developer")
    developers = [d.__name__.split(".")[-1] for d in bsp_tool.branches.developers]
    db.executemany("INSERT INTO Developer(name) VALUES(?)", [(d,) for d in developers])

    tables.append("Engine")
    engines = list(bsp_tool.branches.of_engine.keys())
    db.executemany("INSERT INTO Engine(name) VALUES(?)", [(e,) for e in engines])

    tables.append("Branch")
    branches = list()
    engine_of = {
        branch: engine
        for engine, branches in bsp_tool.branches.of_engine.items()
        for branch in branches}
    with open("branch.data.colour.json") as json_file:
        colours = json.load(json_file)
    for developer_index, developer in enumerate(bsp_tool.branches.developers):
        for branch in developer.scripts:
            developer_name, branch_name = branch.__name__.split(".")[-2:]
            engine_index = engines.index(engine_of[branch])
            colour = colours[developer_name][branch_name]
            branches.append((branch_name, developer_index + 1, engine_index + 1, colour))
    db.executemany("INSERT INTO Branch(name, developer, engine, colour) VALUES(?, ?, ?, ?)", branches)
    branch_names = [name for name, developer, engine, colour in branches]

    tables.append("BranchFork")
    forks = list()
    with open("branch.data.fork.json") as json_file:
        for base_branch, fork_branches in json.load(json_file).items():
            base_branch_index = branch_names.index(base_branch)
            for fork_branch in fork_branches:
                forks.append((base_branch_index + 1, branch_names.index(fork_branch) + 1))
    db.executemany("INSERT INTO BranchFork(base, fork) VALUES(?, ?)", forks)

    common.tables_to_file(db, "branch.data.sql", tables)


def load_into(database: sqlite3.Connection):
    common.run_script(database, "branch.tables.sql")
    common.run_script(database, "branch.data.sql")


# queries
def module_index(db: sqlite3.Connection, branch: ModuleType) -> int:
    developer_name, branch_name = branch.__name__.split(".")[-2:]
    query = ["SELECT B.rowid FROM Branch as B",
             "JOIN Developer as D ON B.developer = D.rowid",
             "WHERE B.name = ? AND D.name = ?"]
    db.execute("\n".join(query), [branch_name, developer_name])


if __name__ == "__main__":
    generate()  # writes to branch.data.sql
