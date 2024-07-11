import importlib
import json
import os

import bsp_tool


def bsp_tool_git_sha() -> str:
    path = bsp_tool.__path__[0]
    version = importlib.metadata.metadata("bsp_tool").json["version"]
    assert os.path.isdir(f"{path}-{version}.dist-info")
    with open(os.path.join(f"{path}-{version}.dist-info", "direct_url.json")) as json_file:
        direct_url_json = json.load(json_file)
    # direct_url_json = {
    #     "url": "https://github.com/snake-biscuits/bsp_tool.git",
    #     "vcs_info": {
    #         "commit_id": "f7f7c7aac31709efff56e6cbf81cdd2332e51900",
    #         "vcs": "git"}}
    assert "vcs_info" in direct_url_json
    assert direct_url_json["vcs_info"]["vcs"] == "git"
    assert "commit_id" in direct_url_json["vcs_info"]  # TODO: allow tags
    sha = direct_url_json["vcs_info"]["commit_id"]
    return sha[:7]
