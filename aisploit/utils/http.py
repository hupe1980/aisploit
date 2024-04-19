def cookies_as_dict(cookies: str) -> dict:
    """
    Convert a string of cookies into a dictionary.
    """
    return {key_value.strip().split("=")[0]: "=".join(key_value.split("=")[1:]) for key_value in cookies.split(";")}
