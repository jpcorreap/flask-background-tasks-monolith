import os

from celery import Celery
import ffmpeg
from models.submission import Submission, SubmissionStatus
from models.user import User
from settings import PROCESSED_FOLDER_PATH, PROCESSING_FOLDER_PATH
from utils.db import db_session

from backend.email.email_sender import send_many_emails

app = Celery("tasks", broker="redis://localhost:6379/0")


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
        "{fpath}/{filename}".format(fpath=PROCESSING_FOLDER_PATH, filename=filename)
    )
    ffmpeg.output(
        input,
        "{new_path}/{name}.mp3".format(new_path=PROCESSED_FOLDER_PATH, name=name),
        format="mp3",
    ).run(overwrite_output=True)
    os.remove(
        "{fpath}/{filename}".format(fpath=PROCESSING_FOLDER_PATH, filename=filename)
    )
    print("\n-> El archivo convertir se copió a : {}".format(PROCESSED_FOLDER_PATH))


@app.task(base=SqlAlchemyTask)
def process_audio_files():
    pending_submissions = (
        db_session.query(Submission)
        .filter_by(status=SubmissionStatus.processing)
        .join(User, Submission.user_id == User.id)
        .all()
    )

    if pending_submissions:
        for i in pending_submissions:
            filename = "{id}.{file_type}".format(id=i.id, file_type=i.file_type)
            try:
                convert_to_mp3(filename)
                i.status = SubmissionStatus.converted
            except Exception as e:
                print(e)

        converted_submissions = list(
            filter(
                lambda x: (x.status == SubmissionStatus.converted), pending_submissions
            )
        )
        db_session.add_all(converted_submissions)
        db_session.commit()

        users_emails = [submission.user.email for submission in converted_submissions]

        send_many_emails(
            users_emails, "Your Submission has been converted successfully"
        )


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls process_audio_files every 15 minutes.
    sender.add_periodic_task(
        900, process_audio_files.s(), name="Process Files every 2 minutes"
    )
