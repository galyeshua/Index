from app import app, db
from flask import render_template


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def error_500(error):
    db.session.remove()
    return render_template('errors/500.html'), 500


@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html'), 413
