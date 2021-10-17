from flask import Blueprint
from .resources import AdvertisementApi

portal_bp = Blueprint('portal', __name__, template_folder='templates')
api_bp = Blueprint('api', __name__, url_prefix='/api/v1/advertisement')
api_bp.add_url_rule('', view_func=AdvertisementApi.as_view('advertisements'))
api_bp.add_url_rule('/<title>', view_func=AdvertisementApi.as_view('advertisement_by_title'))

from . import routes
