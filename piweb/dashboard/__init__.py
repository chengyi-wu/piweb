from flask import Flask, Blueprint, render_template
from .. import api

bp = Blueprint("dashboard", __name__, url_prefix="/")

@bp.route("/")
def index():
    disk_total, disk_used, disk_free = api.disk_usage("/").split()
    return render_template(
        "dashboard/index.html",
        temperature = api.measure_temp(),
        disk_total = float(disk_total),
        disk_used = float(disk_used),
    )

@bp.route("/ps")
def ps():
    data = []
    for row in api.ps().decode('utf-8').split("\n"):
        row = row.split()
        if len(row) < 4 or row[0] == "USER": continue
        data += [
            {
                "USER": row[0],
                "PID" : row[1],
                "%CPU": row[2],
                "%MEM": row[3],
                "TIME": row[9],
                "COMMAND" : " ".join(row[10:])
            }
        ]
    return render_template(
        "dashboard/process.html",
        data = data[:10]
    )