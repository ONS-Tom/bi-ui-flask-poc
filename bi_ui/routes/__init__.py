from bi_ui import app
from bi_ui.routes.authentication import authentication_bp


app.register_blueprint(authentication_bp, url_prefix='/auth/')