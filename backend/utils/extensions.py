from constants.extensions import ALLOWED_EXTENSIONS


def allowed_file(filename, file_type):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]
    )
