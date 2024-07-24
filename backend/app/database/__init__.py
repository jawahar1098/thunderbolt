from flask import Blueprint



database_bp = Blueprint('database_bp', __name__)

from app.database import routes