from flask import Flask, Blueprint
from subprocess import Popen, PIPE
import shutil, json
from .pms5003t import Sensor

sensor = Sensor()

bp = Blueprint("api", __name__, url_prefix="/api")

def shell_exec(cmd:str):
    with Popen(cmd, shell=True, stdout=PIPE) as proc:
        return proc.stdout.read()

@bp.route("/measure_temp", methods=["GET"])
def measure_temp():
    import random
    return str(random.randint(0, 100))
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        return "%d" % (int(f.read().strip()) // 1000)

@bp.route("/ps", methods=["GET"])
def ps():
    return shell_exec("ps aux | sort -nrk 3,3")

def disk_usage(disk):
    gb = 2 ** 30
    total, used, free = shutil.disk_usage(disk)
    return "%.2f %.2f %.2f" % (total / gb, used / gb, free / gb)

@bp.route("/pms", methods=["GET"])
def pms():
    data = {}
    data['pm1_cf'] = "N/A"
    data['pm25_cf'] = "N/A"
    data['pm10_cf'] = "N/A"
    data['temperature'] = "N/A"
    data['humidity'] = "N/A"
    try:
        sensor.open()
        data = sensor.read()
        sensor.close()
    except:
        pass
    return json.dumps(data)