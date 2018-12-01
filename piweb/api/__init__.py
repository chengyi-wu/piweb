from flask import Flask, Blueprint
from subprocess import Popen, PIPE
import shutil

bp = Blueprint("api", __name__, url_prefix="/api")

def shell_exec(cmd:str):
    with Popen(cmd, shell=True, stdout=PIPE) as proc:
        return proc.stdout.read()

@bp.route("/measure_temp", methods=["GET"])
def measure_temp():
    return "10"
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        return "%d" % (int(f.read().strip()) // 1000)

@bp.route("/ps", methods=["GET"])
def ps():
    return shell_exec("ps aux | sort -nrk 3,3")

def disk_usage(disk):
    gb = 2 ** 30
    total, used, free = shutil.disk_usage(disk)
    return "%.2f %.2f %.2f" % (total / gb, used / gb, free / gb)