from bi_ui import app
from bi_ui.views.home import home_bp
from bi_ui.views.login import login_bp
from bi_ui.views.results import results_bp
from bi_ui.views.errors import error_bp


app.register_blueprint(login_bp, url_prefix='/')
app.register_blueprint(home_bp, url_prefix='/Home')
app.register_blueprint(results_bp, url_prefix='/Results')
app.register_blueprint(error_bp, url_prefix='/Error')