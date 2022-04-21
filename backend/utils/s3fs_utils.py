import s3fs

BUCKET_NAME = "test-python-boto3-cloud"


def get_client():
    return s3fs.S3FileSystem(
        #key="",
        #secret="",
        #token=""
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


def download_file(s3_path, system_path):
    fs = get_client()
    fs.download(f'{BUCKET_NAME}/{s3_path}', system_path)