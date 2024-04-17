"""API V1 Blueprint"""

import logging

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import (
    BadRequest,
    Unauthorized,
    InternalServerError,
    MethodNotAllowed,
    Conflict,
)

from db import connect
from models import Entities
from prove_of_ownership import ProveOfOwnership
from utils import generate_eid

v1_blueprint = Blueprint("v3", __name__, url_prefix="/api//v1")

logger = logging.getLogger(__name__)

database = connect()


def set_security_headers(response):
    """Set security headers for each response."""
    security_headers = {
        "Strict-Transport-Security": "max-age=63072000; includeSubdomains",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "script-src 'self'; object-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Cache-Control": "no-cache",
        "Permissions-Policy": (
            "accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), camera=(), "
            "clipboard-read=(), clipboard-write=(), cross-origin-isolated=(), display-capture=(), "
            "document-domain=(), encrypted-media=(), execution-while-not-rendered=(), "
            "execution-while-out-of-viewport=(), fullscreen=(), gamepad=(), geolocation=(), "
            "gyroscope=(), magnetometer=(), microphone=(), midi=(), navigation-override=(), "
            "payment=(), picture-in-picture=(), publickey-credentials-get=(), screen-wake-lock=(), "
            "speaker=(), speaker-selection=(), sync-xhr=(), usb=(), web-share=(), "
            "xr-spatial-tracking=()"
        ),
    }

    for header, value in security_headers.items():
        response.headers[header] = value

    return response


@v1_blueprint.before_request
def before_request():
    """Connect to the database before each request."""
    if not database.is_closed():
        database.close()
    database.connect()


@v1_blueprint.after_request
def after_request(response):
    """Close the database connection and set security headers after each request."""
    if not database.is_closed():
        database.close()
    response = set_security_headers(response)
    return response


@v1_blueprint.route("/entities", methods=["POST", "PUT"])
def create_entity():
    """Create an entity."""
    if not request.json.get("msisdn"):
        raise BadRequest("MSISDN is Required")

    msisdn = request.json["msisdn"]
    verifier = ProveOfOwnership()

    existing_entity_msisdn = Entities.get_or_none(msisdn_hash=msisdn)
    if existing_entity_msisdn:
        raise Conflict("Entity MSISDN already exists")

    if request.method.lower() == "post":
        if verifier.send_verification_code(phone_number=msisdn):
            return jsonify({}), 201

        raise InternalServerError()

    if request.method.lower() == "put":
        if not request.json.get("code"):
            raise BadRequest("Code is Required")

        if not request.json.get("password"):
            raise BadRequest("Password is Required")

        if not request.json.get("username"):
            raise BadRequest("Username is Required")

        code = request.json["code"]
        password = request.json["password"]
        username = request.json["username"]

        existing_entity_username = Entities.get_or_none(username=username)
        if existing_entity_username:
            raise Conflict("Entity Username already exists")

        if verifier.verify_code(phone_number=msisdn, code=code):
            eid = generate_eid(username=username, msisdn=msisdn)
            entity = Entities.create(
                eid=eid, msisdn_hash=msisdn, username=username, password_hash=password
            )

            return jsonify({"eid": entity.eid}), 200

        raise Unauthorized("Incorrect code")

    raise MethodNotAllowed()


@v1_blueprint.errorhandler(MethodNotAllowed)
@v1_blueprint.errorhandler(Unauthorized)
@v1_blueprint.errorhandler(BadRequest)
@v1_blueprint.errorhandler(Conflict)
def handle_client_errors(error):
    """Handle client errors."""
    logger.error(error.description)
    return jsonify({"error": error.description}), error.code


@v1_blueprint.errorhandler(InternalServerError)
@v1_blueprint.errorhandler(Exception)
def handle_general_server_error(error):
    """Handle General Server errors."""
    logger.exception(error)
    return (
        jsonify({"error": "Oops, something went wrong, please try again later"}),
        500,
    )
