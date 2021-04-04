from flask import abort, Blueprint, jsonify, request
from . import device

bp = Blueprint("router", __name__)


@bp.route("/", methods=["GET"])
def get_all():
    start = request.args.get("start")
    end = request.args.get("end")
    cols = request.args.get("columns")
    devs = device.get_all(start, end, cols)
    return jsonify(devs)


@bp.route("/<name>", methods=["GET"])
def get_one(name):
    start = request.args.get("start")
    end = request.args.get("end")
    cols = request.args.get("columns")
    dev = device.get_one(name, start, end, cols)

    if not dev:
        abort(404)

    return dev


def cors(res):
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res


bp.after_request(cors)
