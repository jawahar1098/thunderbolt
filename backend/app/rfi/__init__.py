from flask import Blueprint



rfi_bp = Blueprint('rfi_bp', __name__)

from app.rfi import routes