from ..utils.api_resource import ApiResource
from .models import Advertisement

from .schemas import AdvertisementSchema


class AdvertisementApi(ApiResource):
    MODEL_CLASS = Advertisement
    SCHEMA_CLASS = AdvertisementSchema()
