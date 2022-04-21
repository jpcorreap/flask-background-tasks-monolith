import s3fs

BUCKET_NAME = "supervoices7"


def get_client():
    return s3fs.S3FileSystem(
        #  key="",
        #  secret="",
        #  token=""
        # Accessing all buckets you have access to with your credentials
        anon=False
    )


def list_files(fs_client):
    print("------- ARCHIVOS EN EL BUCKET ----------")
    print(fs_client.ls(BUCKET_NAME))


def upload_file(file_in_bytes, folder, final_name):
    try:
        fs = get_client()
        with fs.open(f"s3://{BUCKET_NAME}/{folder}/{final_name}", "wb") as s3_obj:
            s3_obj.write(file_in_bytes)
        return True

    except Exception as e:
        print(str(e))
        return False


def get_signed_url(folder, final_name) -> str:
    fs = get_client()
    signed_url = fs.sign(
        f"s3://{BUCKET_NAME}/{folder}/{final_name}", client_method="get_object"
    )
    return signed_url


def get_presigned_url(folder, final_name) -> str:
    fs = get_client()
    presigned_url = fs.url(
        f"s3://{BUCKET_NAME}/{folder}/{final_name}", client_method="put_object"
    )
    return presigned_url


def download_file(s3_path, system_path):
    fs = get_client()
    fs.download(f"{BUCKET_NAME}/{s3_path}", system_path)
