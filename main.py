import hashlib
import json
import os
import os.path
import zipfile

import requests

index = {
    "formatVersion": 1,
    "game": "minecraft",
    "versionId": "",
    "name": "",
    "summary": "",
    "dependencies": {
        "minecraft": "",
        "forge": ""
    },
    "files": []
}
files = []

config = {}


def get_hash(fn: str, hash_type) -> str:
    h = hash_type
    with open(fn, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def unzip_modpack(filename: str) -> None:
    if not os.path.isdir(".cache"):
        os.mkdir(".cache")
    with zipfile.ZipFile(filename, mode="r") as f:
        for file in f.namelist():
            f.extract(file, os.getcwd() + "\\.cache")


# TODO: 查找模组链接等信息
def add_mod(mod_hash: dict, filename: str) -> dict:
    header = {
        "User-Agent": "Ginsway/project_name/1.0.0"
    }
    url = "https://api.modrinth.com/v2/version_file/"
    response = requests.get(url + mod_hash["sha1"], headers=header)
    if not response.text:
        return {}
    result = response.json()
    for i in result["files"]:
        if (i["filename"]) == filename:
            file = {"path": f"mods/{filename}", "downloads": [i["url"]],
                    "fileSize": i["size"], "hashes": {
                    "sha1": mod_hash["sha1"],
                    "sha512": mod_hash["sha512"]
                }}
            break
    return file


def get_pack_info() -> None:
    with open(".cache/manifest.json", "r") as f:
        result = f.read()
        result = json.loads(result)
        index["versionId"] = result["version"]
        index["name"] = result["name"]


def del_cache(dir: str) -> None:
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(dir)


def get_loader() -> None:
    with open(".cache/mcbbs.packmeta", "r", encoding="utf-8") as f:
        result = f.read()
        result = json.loads(result)
        for i in result["addons"]:
            if i["id"] == "game":
                index["dependencies"]["minecraft"] = i["version"]
            if i["id"] == "forge":
                index["dependencies"]["forge"] = i["version"]


def main() -> None:
    unzip_modpack(input("modpack"))
    print("正在解压原整合包")
    for i in os.listdir(".cache/overrides/mods"):
        sha1 = get_hash(f"{os.getcwd()}\\.cache\\overrides\\mods\\{i}", hashlib.sha1())
        sha512 = get_hash(f"{os.getcwd()}\\.cache\\overrides\\mods\\{i}", hashlib.sha512())
        modinfo = add_mod({"sha1": sha1, "sha512": sha512}, i)
        if modinfo:
            print(f"添加了modrinth模组文件：{i}")
            files.append(modinfo)
            os.remove(f".\\.cache\\overrides\\mods\\{i}")
    # print(files)
    index["files"] = files
    print("开始编写整合包索引")
    get_pack_info()
    get_loader()
    with open("./.cache/overrides/modrinth.index.json", "w") as i:
        i.write(json.dumps(index))
    print("编写整合包索引完毕")
    print("开始重新打包")
    with zipfile.ZipFile("modpack.mrpack", "w") as f:
        for path, dir_lst, file_lst in os.walk(r"./.cache/overrides"):
            for file in file_lst:
                f.write(f"{path}/{file}", f"{path.replace(r'./.cache/', './')}/{file}")
        f.write(r"./.cache/overrides/modrinth.index.json", f"modrinth.index.json")
    del_cache(".cache")
    print("打包完成")


if __name__ == "__main__":
    main()
