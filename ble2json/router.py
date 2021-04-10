from flask import abort, Blueprint, jsonify, request
from . import device, error

bp = Blueprint("router", __name__)


@bp.route("/", methods=["GET"])
def get_all():
    error.check()
    start = request.args.get("start")
    end = request.args.get("end")
    cols = request.args.get("columns")
    devs = device.get_all(start, end, cols)
    return jsonify(devs)


@bp.route("/errors", methods=["GET"])
def get_errors():
    errors = error.get_all()
    return jsonify(errors)


@bp.route("/<name>", methods=["GET"])
def get_one(name):
    error.check()
    start = request.args.get("start")
    end = request.args.get("end")
    cols = request.args.get("columns")
    dev = device.get_one(name.lower(), start, end, cols)

    if not dev:
        abort(404)

    return dev
