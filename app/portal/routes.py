import logging

from flask import render_template

from . import portal_bp

logger = logging.getLogger(__name__)


@portal_bp.route("/")
def index():
    return render_template("index.html")
