def validate_url(url):
    wrong_characters = [" ", "ñ"]
    for character in wrong_characters:
        if character in url:
            return False
    return True
