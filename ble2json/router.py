from flask import abort, Blueprint, jsonify, request
from . import device

bp = Blueprint("router", __name__)


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

    abort(404)


def cors(res):
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res


bp.after_request(cors)
