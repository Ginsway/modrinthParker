import getopt
import hashlib
import sys
from os import mkdir, getcwd
from zipfile import ZipFile
from typing import BinaryIO

index = {}

config = {}


def get_hash(f: BinaryIO) -> str:
    h = hashlib.sha1()
    h.update(f)
    return h.hexdigest()


def unzip_modpack(filename: str):
    mkdir(".cache")
    with ZipFile(filename, mode="r") as f:
        for file in f.namelist():
            f.extract(file, getcwd() + "\\.cache")


# TODO: 查找模组链接等信息
def get_file():
    pass


def get_argv(argv):
    short_opts = "hv"
    long_opts = ["help", "verbose"]
    try:
        opts, args = getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError:
        print("Invalid command line arguments")
        sys.exit(2)

    # 处理选项
    verbose = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage: python myprogram.py [-h|--help] [-v|--verbose] [file ...]")
            sys.exit()
        elif opt in ("-v", "--verbose"):
            verbose = True

    # 处理参数
    for arg in args:
        print("Processing file:", arg)

    # 打印选项和参数
    print("Verbose mode:", verbose)
    print("Remaining arguments:", args)


if __name__ == "__main__":
    pass
