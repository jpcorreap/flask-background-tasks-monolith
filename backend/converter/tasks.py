import os

from celery import Celery
import ffmpeg
from models.submission import Submission, SubmissionStatus
from settings import PROCESSED_FOLDER_PATH, PROCESSING_FOLDER_PATH

app = Celery("tasks", broker="redis://localhost:6379/0")


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


@app.task
def process_audio_files():
    pending_submissions = Submission.query.filter_by(
        status=SubmissionStatus.processing
    ).all()

    if pending_submissions:

        for i in pending_submissions:
            filename = "{id}.{file_type}".format(id=i.id, file_type=i.file_type)
            convert_to_mp3(filename)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        120.0, process_audio_files.s(), name="Process Files every 2 minutes"
    )
