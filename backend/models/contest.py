import uuid

from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model
from settings import config


class Contest(Model):
    class Meta:
        table_name = "contest"
        aws_access_key_id = config.AWS_SECRET_ACCESS_KEY
        aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
        aws_session_token = config.AWS_SESSION_TOKEN
        region = config.AWS_REGION

    class AdminIndex(GlobalSecondaryIndex):
        class Meta:
            read_capacity_units = 1
            write_capacity_units = 1
            projection = AllProjection()

        admin = NumberAttribute(hash_key=True, null=False)

    class UrlIndex(GlobalSecondaryIndex):
        class Meta:
            read_capacity_units = 1
            write_capacity_units = 1
            projection = AllProjection()

        url = UnicodeAttribute(hash_key=True, null=False)

    id = UnicodeAttribute(null=False, default=uuid.uuid4, hash_key=True)
    url = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    image_type = UnicodeAttribute(null=False)
    start_date = UTCDateTimeAttribute(null=False)
    end_date = UTCDateTimeAttribute(null=False)
    prize = UnicodeAttribute(null=False)
    script = UnicodeAttribute(null=False)
    advices = UnicodeAttribute(null=False)
    admin = NumberAttribute(null=False)
    url_index = UrlIndex()
    admin_index = AdminIndex()
