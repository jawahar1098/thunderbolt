from flask import Flask
from flask_cors import CORS

sample = "Asdfasdf"
app = Flask(__name__)
def create_app():
    CORS(app)
    # Import and register blueprints
    from app.auth import auth as auth_blueprint
    from app.cdat import cdr_bp as cdat_bluprint
    from app.ticketing import tickect_bp as ticket_blueprint
    from app.database import database_bp as database_blueprint
    # from app.nexus import nexus_bp 
    from app.vigor import vigor_bp
    from app.analysis import analysis_bp
    from app.thunderbolt import thunder_bp
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(cdat_bluprint)
    app.register_blueprint(ticket_blueprint)
    app.register_blueprint(database_blueprint)
    # app.register_blueprint(nexus_bp)
    app.register_blueprint(vigor_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(thunder_bp)

    
    

    return app

