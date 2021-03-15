import gzip
from flask import abort, Blueprint, json, jsonify, request, make_response
from . import device

bp = Blueprint("router", __name__)


@bp.route("/", methods=["GET"])
def get_all():
    start = request.args.get("start")
    end = request.args.get("end")
    cols = request.args.get("columns")
    devs = device.get_all(start, end, cols)

    if "gzip" in request.accept_encodings:
        return compress(devs)

    return jsonify(devs)


@bp.route("/<name>", methods=["GET"])
def get_one(name):
    start = request.args.get("start")
    end = request.args.get("end")
    cols = request.args.get("columns")
    dev = device.get_one(name, start, end, cols)

    if not dev:
        abort(404)

    if "gzip" in request.accept_encodings:
        return compress(dev)

    return dev


def compress(data):
    b = bytes(json.dumps(data), "UTF-8")
    res = make_response(gzip.compress(b))
    res.headers["Content-Type"] = "application/json"
    res.headers["Content-Encoding"] = "gzip"
    return res


def cors(res):
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res


bp.after_request(cors)
