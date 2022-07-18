class EuskalmetException(Exception):
    def __init__(self, msg):
        pass

    def __new__(cls, status, *args, **kwargs):
        try:
            error = int(status["error"])
        except TypeError:
            pass
        reason = status["reason"]
        url = status["url"]
        if error == 401:
            msg = "Unauthorized"
        elif error == 404:
            msg = "Not found"
        elif error == 500:
            msg = "Internal server error"
        else:
            msg = "Unknown error"

        msg = f"Error {error} - {msg}"

        if reason:
            msg += f" ({reason})"

        if url:
            msg += f" - {url}"

        return super().__new__(cls, msg, *args, **kwargs)
