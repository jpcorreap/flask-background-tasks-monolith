import ffmpeg
from settings import config


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
