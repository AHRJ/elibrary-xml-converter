import base64


def extract_xml(event):
    post_data = base64.b64decode(event["body"])
    return post_data.split(b"\r\n")[4].decode("utf-16")
