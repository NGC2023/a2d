from flask import Blueprint, render_template, send_from_directory, redirect, abort
import os

docs_routes = Blueprint('docs', __name__)

DOCUMENTATION_PATH = '/usr/share/doc/a2d-doc/html'

@docs_routes.route('/docs/<path:filename>')
def serve_docs(filename):
    try:
        return send_from_directory(DOCUMENTATION_PATH, filename)
    except FileNotFoundError:
        abort(404)

@docs_routes.route('/info')
def info():
    index_file = os.path.join(DOCUMENTATION_PATH, 'index.html')
    if os.path.exists(index_file):
        return redirect('/docs/index.html', code=302)
    else:
        return render_template('no_docs.html')
