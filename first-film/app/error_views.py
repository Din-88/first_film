
from flask import render_template
from flask import current_app as app

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html')

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')