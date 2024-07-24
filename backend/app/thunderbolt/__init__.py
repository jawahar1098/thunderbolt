from flask import Blueprint



thunder_bp = Blueprint('thunder_bp', __name__)

from app.thunderbolt import routes