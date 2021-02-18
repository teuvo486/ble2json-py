from flask import abort, Blueprint, jsonify, request
from . import db, device

bp = Blueprint("device", __name__)


@bp.route("/", methods=["GET"])
def get_all():
    start = request.args.get("start")
    end = request.args.get("end")

    dev = device.get_all(start, end)

    return jsonify(dev)


@bp.route("/<name>", methods=["GET"])
def get_one(name):
    start = request.args.get("start")
    end = request.args.get("end")

    dev = device.get_one(name, start, end)

    if dev:
        return dev
    else:
        abort(404)
