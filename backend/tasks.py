import os

from celery import Celery
from custom_email.email_sender import send_many_emails
import ffmpeg
from models.admin import Admin
from models.contest import Contest
from models.submission import Submission, SubmissionStatus
from models.user import User
from settings import config
from utils.db import db_session

app = Celery("tasks", broker="redis://redis:6379/0")


class SqlAlchemyTask(app.Task):
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


@app.task(base=SqlAlchemyTask)
def process_audio_files():
    pending_submissions = (
        db_session.query(Submission, User)
        .filter_by(status=SubmissionStatus.processing)
        .join(User.submissions)
        .all()
    )

    if pending_submissions:
        for (submission, _) in pending_submissions:
            filename = "{id}.{file_type}".format(
                id=submission.id, file_type=submission.file_type
            )
            try:
                convert_to_mp3(filename)
                submission.status = SubmissionStatus.converted
            except Exception as e:
                print(e)

        converted_submissions = list(
            filter(
                lambda xy: (xy[0].status == SubmissionStatus.converted),
                pending_submissions,
            )
        )

        db_session.add_all(map(lambda xy: xy[0], converted_submissions))
        db_session.commit()

        users_emails = [user.email for _, user in converted_submissions]

        """send_many_emails(
            users_emails, "Your Submission has been converted successfully"
        )"""


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls process_audio_files every 5 minutes.
    sender.add_periodic_task(
        300, process_audio_files.s(), name="Process Files every 5 minutes"
    )
