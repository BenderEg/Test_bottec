from core.const import base_buttons
from db.shemas import User
from services.base_service import BaseService


class BucketService(BaseService):

    def show_bucket_itmes(self, bucket: dict) -> str:
        sorted_bucket = sorted(bucket.values(), key=lambda x: x.get('name'))
        res = ''
        return sorted_bucket