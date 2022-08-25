#!/usr/bin/python3
"""
2. Deploy archive!
"""
from fabric.api import *
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['54.224.105.134', '34.239.247.122']


def do_clean(number=0):
    """
    Delete old releases
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
