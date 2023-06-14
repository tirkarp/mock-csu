import copy
import json

from flask import Flask, send_file

app = Flask(__name__)


with open("periodicUDSConfigChanges.json") as f:
    uds_config_changes_content = f.read()

uds_config_changes = json.loads(uds_config_changes_content)
original_uds_config_changes = copy.deepcopy(uds_config_changes)


@app.route("/")
def hello():
    return "HELLO"


@app.route("/reset")
def reset():
    global uds_config_changes
    uds_config_changes = copy.deepcopy(original_uds_config_changes)
    return ("OK", 200)


@app.route("/periodicUDSConfigChanges")
def periodicUDSConfigChanges():
    return uds_config_changes


@app.route("/periodicUDSConfigStatus/<esn>/<int:address>/<box_id>")
def periodicUDSConfigStatus(esn, address, box_id):
    l = uds_config_changes["udsConfigChanges"]
    index = [i for i, x in enumerate(l) if x["esn"] == esn and x["addrs"][0] == address and x["boxID"] == box_id]

    if not index:
        return ("Not Found", 404)
    else:
        uds_config_changes["udsConfigChanges"].pop(index[0])
        return ("OK", 200)
    

@app.route("/cals/calStatus/<esn>/<int:address>/<box_id>")
def calStatus(esn, address, box_id):
    return ("OK", 200)


@app.route("/cals/pendingCal/<esn>/<int:address>/ZIP")
def pendingCal(esn, address):
    return send_file("67384768_0.zip", "application/zip")


@app.route("/paccar-200")
def paccar_200():
    return ("OK", 200)


@app.route("/paccar-404")
def paccar_404():
    return ("Not Found", 404)