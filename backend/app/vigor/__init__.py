from flask import Blueprint
from flask_cors import CORS
vigor_bp = Blueprint('vigor_bp', __name__)


from app.vigor import routes

# from app.ticketing import *
# from app.ticketing.endpointsimport *

CORS(vigor_bp)