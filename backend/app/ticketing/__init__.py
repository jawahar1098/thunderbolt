from flask import Blueprint
# from flask_cors import CORS
tickect_bp = Blueprint('tickect_bp', __name__)


from app.ticketing import routes

# from app.ticketing import *
# from app.ticketing.endpointsimport *
