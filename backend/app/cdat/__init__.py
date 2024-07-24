from flask import Blueprint



cdr_bp = Blueprint('cdr_bp', __name__)

from app.cdat import routes