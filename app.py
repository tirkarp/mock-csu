import copy
import json
import time

from flask import Flask, request, send_file

app = Flask(__name__)


# periodicUDSConfigChanges
with open("periodicUDSConfigChanges.json") as f:
    uds_config_changes_content = f.read()

uds_config_changes = json.loads(uds_config_changes_content)
original_uds_config_changes = copy.deepcopy(uds_config_changes)


# periodicUDSConfig
with open("periodicUDSConfig.json") as f:
    uds_config_content = f.read()

uds_config = json.loads(uds_config_content)
original_uds_config = copy.deepcopy(uds_config)


# routing
@app.route("/")
def hello():
    return "HELLO"


@app.route("/reset")
def reset():
    global uds_config_changes
    uds_config_changes = copy.deepcopy(original_uds_config_changes)

    global uds_config
    uds_config = copy.deepcopy(original_uds_config)

    return ("OK", 200)


@app.route("/add-esn", methods=["GET", "POST"])
def add_esn():
    esn_obj = request.get_json(force=True)
    uds_config_changes["udsConfigChanges"].append(esn_obj)
    return ("OK", 200)


@app.route("/periodicUDSConfigChanges")
def periodicUDSConfigChanges():
    return uds_config_changes


@app.route("/periodicUDSConfig/<esn>/<int:address>")
def periodicUDSConfig(esn: str, address: int):
    uds_config["esn"] = esn
    uds_config["addr"] = address

    esn_obj_list = [x for x in uds_config_changes["udsConfigChanges"] if x["esn"] == esn]

    if esn_obj_list:
        esn_obj = esn_obj_list[0]
        uds_config["boxID"] = esn_obj["boxID"]

        if esn_obj["operation"] == "DELETE":
            return ("Cannot download DELETE config", 500)

    return uds_config


@app.route("/periodicUDSConfigStatus/<esn>/<int:address>/<box_id>")
def periodicUDSConfigStatus(esn: str, address: int, box_id: str):
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


@app.route("/paccar-200/supplierti", methods=["GET", "POST"])
def paccar_200():
    return ("OK", 200)


@app.route("/paccar-404/supplierti", methods=["GET", "POST"])
def paccar_404():
    return ("Not Found", 404)


@app.route("/paccar-400/supplierti", methods=["GET", "POST"])
def paccar_400():
    return ("Bad Request", 400)


@app.route("/paccar-401/supplierti", methods=["GET", "POST"])
def paccar_401():
    return ("Unauthorized", 401)


@app.route("/timeout", methods=["GET", "POST"])
def paccar_timeout():
    time.sleep(100)
    return ("This should be 408 or 502, not 200. Timeout test failed.", 200)


@app.route("/timeout/<int:val>", methods=["GET", "POST"])
def paccar_timeout_value(val):
    time.sleep(val)
    return ("This should be 408 or 502, not 200. Timeout test failed.", 200)