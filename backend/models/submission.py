from enum import Enum
import uuid

from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model
from settings import config


class SubmissionStatus(str, Enum):
    processing = "processing"
    converted = "converted"


class SubmissionFileType(str, Enum):
    mp3 = "mp3"
    wav = "wav"
    m4a = "m4a"
    mpc = "mpc"
    wma = "wma"


class Submission(Model):
    class Meta:
        table_name = "submission"
        region = config.AWS_REGION
        aws_access_key_id = config.AWS_ACCESS_KEY_ID
        aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
        aws_session_token = config.AWS_SESSION_TOKEN

    class ContestIdIndex(GlobalSecondaryIndex):
        class Meta:
            read_capacity_units = 1
            write_capacity_units = 1
            projection = AllProjection()

        contest_id = UnicodeAttribute(hash_key=True, null=False)

    id = UnicodeAttribute(null=False, default=uuid.uuid4, hash_key=True)
    user_id = NumberAttribute(null=False)
    observations = UnicodeAttribute(null=False)
    status = UnicodeAttribute(null=False)
    contest_id = UnicodeAttribute(null=False)
    upload_date = UTCDateTimeAttribute(null=False)
    file_type = UnicodeAttribute(null=False)
    contest_id_index = ContestIdIndex()
    user_name = UnicodeAttribute(null=False)
    user_email = UnicodeAttribute(null=False)
