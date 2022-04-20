import s3fs

BUCKET_NAME = "test-python-boto3-cloud"


def get_client():
    return s3fs.S3FileSystem(
        # key="ASIA5TXLE3M6TDNTCRMN",
        # secret="av+gPloLvgdNUHUPd7OFH779lxB+KV0QNTwRC+lS",
        # token="FwoGZXIvYXdzEGIaDKaSszLKUkSNMjaKqCLKAW++UD/W57UT4uXxLhncIuulYWEWmfKEjadff/wj8DV9K4ORhL93vieRWHAtdMXpDrcIE4YZSVhLPmO6SXDdrtjSwewuHR/PJG2l4cOiuS7EJCH13mm3FVfoB2lJNzx6d/2xRK4U3J/RMbv8gUpYNSmDTtA6qG75Itp4wPieM8jCrO7vBcGAS5UfAMsfGOyDaPcOgwo3kGa/AQpL2EQn0cdAAN6BHsAq3wj67gCAtNUsiwELj/6aLknkdW2+vCvhXOXhg5HVQdkNfkQorLD9kgYyLaXQ8sAeEVDbUuaFvx62Jjq/d2mFkw3bL+5IEPumMWu+K0347ECeUTdwnUL1lA=="
        # Accessing all buckets you have access to with your credentials
        anon=False
    ) 


def upload_file(file_in_bytes, folder, final_name):
    try:
        fs = get_client()
        print("Antes:")
        print(fs.ls(BUCKET_NAME))

        with fs.open(f"s3://{BUCKET_NAME}/{folder}/{final_name}", "wb") as s3_obj:
            s3_obj.write(file_in_bytes)

        print("Ahora:")
        print(fs.ls(BUCKET_NAME))

        return True

    except Exception as e:

        print(str(e))
        return False
