import hashlib
import hmac
import base64
from dotenv import load_dotenv
import os
import logging
import json

load_dotenv()
logging.basicConfig(
    filename="sig_validation.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

shared_secret = os.getenv("SHARED_SECRET")
x_sig_in_resp = os.getenv("X_SIG_IN_POSTBACK")
date_in_resp = os.getenv("DATE_IN_POSTBACK")
content_type_in_resp = os.getenv("CONTENT_TYPE_IN_POSTBACK")
resp = os.getenv("POSTBACK_MESSAGE")
request_uri = os.getenv("POSTBACK_URL")


def verify_sig_sha512():
    hashed_resp = hashlib.sha512(resp.encode())
    logging.info(f"Hashed payload: {hashed_resp.hexdigest()}")
    message = (
        "POST"
        + "\n"
        + hashed_resp.hexdigest()
        + "\n"
        + content_type_in_resp
        + "\n"
        + date_in_resp
        + "\n"
        + request_uri
    )
    logging.debug(f"Concatenated message: \n{message}")
    sig = base64.b64encode(
        hmac.new(
            shared_secret.encode(),
            msg=message.encode(),
            digestmod=hashlib.sha512,
        ).digest()
    ).decode()
    logging.info(f"Signature generated: {sig}")
    logging.info(f"Signature matches: {sig==x_sig_in_resp}")


def verify_sig_md5():
    hashed_resp = hashlib.md5(resp.encode())
    logging.info(f"Hashed payload: {hashed_resp.hexdigest()}")
    message = (
        "POST"
        + "\n"
        + hashed_resp.hexdigest()
        + "\n"
        + content_type_in_resp
        + "\n"
        + date_in_resp
        + "\n"
        + request_uri
    )
    logging.debug(f"Concatenated message: \n{message}")
    sig = base64.b64encode(
        hmac.new(
            shared_secret.encode(),
            msg=message.encode(),
            digestmod=hashlib.sha512,
        ).digest()
    ).decode()
    logging.info(f"Signature generated: {sig}")
    logging.info(f"Signature matches: {sig==x_sig_in_resp}")
