import os
import traceback
from flask import Blueprint, request, jsonify, send_file

# local imports
from app.models import ButtonStatus, Devices

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return "Hello World\n"


@main.route("/button-status", methods=["GET", "POST"])
def button_status():
    try:
        if request.method == "GET":
            hardware_id = request.args.get("hardwareID")
            if hardware_id:
                btn_status = ButtonStatus.query.filter(
                    ButtonStatus.hardware_id == hardware_id
                ).one_or_none()
                if btn_status:
                    return jsonify(btn_status.format())
                return jsonify(message="Not found"), 404
            return jsonify(message="Please provide hardwareID"), 400
        # Handle POST request
        data = dict(request.get_json())
        hardware_id = data.get("hardwareID", "")
        status = data.get("status", "")
        message = data.get("message", "")

        # add to device table
        if not Devices.query.filter(Devices.hardware_id == hardware_id).one_or_none():
            new_device = Devices(hardware_id)
            new_device.insert()

        btn_status = ButtonStatus.query.filter(
            ButtonStatus.hardware_id == hardware_id
        ).one_or_none()
        if not btn_status:
            new_staus = ButtonStatus(status, hardware_id, message)
            new_staus.insert()
            return jsonify(success=True)
        # update record
        btn_status.hardware_id = hardware_id
        btn_status.status = status
        btn_status.message = message
        btn_status.update()
        return jsonify(success=True)
    except:
        print(traceback.format_exc())
        return jsonify(success=False), 500


@main.get("/download")
def download_files():
    hardware_id = request.args.get("hardwareID")
    if hardware_id:
        if Devices.query.filter(Devices.hardware_id == hardware_id).one_or_none():
            filename = os.path.abspath(os.path.join("downloads", request.args.get("filename", "")))
            if os.path.exists(filename) and not os.path.isdir(filename):
                return send_file(filename, as_attachment=True)
            return jsonify(message="File not found"), 404
        return jsonify(message="Invalid hardware ID"), 401
    return jsonify(message="Please provide hardwareID"), 400
