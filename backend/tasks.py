import os

from celery import Celery
from custom_email.email_sender import send_email
import ffmpeg
from models.admin import Admin
from models.contest import Contest
from models.submission import Submission, SubmissionStatus
from models.user import User
from settings import config
from utils.db import db_session

celery_app = Celery("tasks", broker="redis://redis:6379/0")


class SqlAlchemyTask(celery_app.Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""

    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()


def convert_to_mp3(filename: str):

    print("\n-> Se va a convertir el archivo: {}".format(filename))
    name = filename.split(".")[0]
    input = ffmpeg.input(
        "{fpath}/{filename}".format(
            fpath=config.PROCESSING_FOLDER_PATH, filename=filename
        )
    )
    ffmpeg.output(
        input,
        "{new_path}/{name}.mp3".format(
            new_path=config.PROCESSED_FOLDER_PATH, name=name
        ),
        format="mp3",
    ).run(overwrite_output=True)
    print(
        "\n-> El archivo convertir se copió a : {}".format(config.PROCESSED_FOLDER_PATH)
    )


@celery_app.task(name="tasks.process_audio_files", base=SqlAlchemyTask)
def process_audio_files(sub_id: str, file_type: str, user_email: str):
    submission = db_session.query(Submission).filter_by(id=sub_id).first()
    filename = f"{sub_id}.{file_type}"
    try:
        convert_to_mp3(filename)
        submission.status = SubmissionStatus.converted
        db_session.commit()
        send_email(user_email, "Your Submission has been converted successfully")
    except Exception as e:
        print(e)
