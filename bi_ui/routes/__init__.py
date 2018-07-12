from bi_ui import app
from bi_ui.routes.authentication import authentication_bp
from bi_ui.routes.api import api_bp


app.register_blueprint(authentication_bp, url_prefix='/auth/')
app.register_blueprint(api_bp, url_prefix='/api/')