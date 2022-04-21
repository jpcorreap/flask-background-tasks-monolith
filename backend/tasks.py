import os

from celery import Celery
from custom_email.email_sender import send_email
import ffmpeg
from models.submission import Submission, SubmissionStatus
from settings import config
from utils.s3fs_utils import get_signed_url, upload_file

celery_app = Celery("tasks", broker=config.BROKER_URL)


def convert_to_mp3(filename: str):

    print("\n-> Se va a convertir el archivo: {}".format(filename))
    name = filename.split(".")[0]
    signed_url = get_signed_url(config.PROCESSING_FOLDER_PATH, filename)
    input = ffmpeg.input(signed_url)
    ruta = f"{config.PROCESSED_FOLDER_PATH}/{name}.mp3"

    ffmpeg.output(
        input,
        ruta,
        format="mp3",
    ).run(overwrite_output=True)

    with open(ruta, "rb") as f:
        upload_file(f.read(), config.PROCESSED_FOLDER_PATH, f"{name}.mp3")
    os.remove(ruta)

    print("\n-> El archivo convertir se copió a : {}".format(ruta))


@celery_app.task(name="tasks.process_audio_files")
def process_audio_files(sub_id: str, file_type: str, user_email: str):
    submission = Submission.get(sub_id)
    filename = f"{sub_id}.{file_type}"
    try:
        convert_to_mp3(filename)
        submission.status = SubmissionStatus.converted
        submission.save()
        send_email(user_email, "Your Submission has been converted successfully")
    except Exception as e:
        print(e)
