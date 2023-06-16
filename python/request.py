from datetime import datetime
import requests
import base64
import json
import hashlib
import hmac
import os
from dotenv import load_dotenv
import logging


load_dotenv()
logging.basicConfig(
    filename="request.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
shared_secret = os.getenv("SHARED_SECRET")
api_username = os.getenv("API_USERNAME")
api_password = os.getenv("API_PASSWORD")
callback_url = os.getenv("CALLBACK_URL")


def debit_wo_signature(merchant_txn_id):
    url = f"{base_url}/transaction/{api_key}/debit"
    user_pass = f"{api_username}:{api_password}"
    encoded_user_pass = base64.b64encode(user_pass.encode()).decode()
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {encoded_user_pass}",
    }
    payload = json.dumps(
        {
            "merchantTransactionId": merchant_txn_id,
            "amount": "9.99",
            "currency": "AUD",
            "callbackUrl": callback_url,
        }
    )
    logging.debug(f"URL: {url}")
    logging.debug(f"Headers: \n{headers}")
    logging.debug(f"Payload: \n{payload}")
    resp = requests.post(url=url, headers=headers, data=payload)
    logging.debug(f"Response status: {resp.status_code}")
    logging.debug(f"Response: {resp.text}")
    try:
        logging.info(
            "Redirect URL: " + resp.json()["redirectUrl"].replace("\\", "")
        )
    except KeyError:
        logging.warning(
            "The result is not as expected. Please change the logging level to"
            " debug."
        )


def generate_signature(merchant_txn_id):
    payload = {
        "merchantTransactionId": merchant_txn_id,
        "amount": "9.99",
        "currency": "AUD",
        "callbackUrl": callback_url,
    }
    shrinked_payload = str(payload).replace(" ", "").replace("'", '"')
    hashed_payload = hashlib.sha512(shrinked_payload.encode())
    logging.info(f"Hashed payload: {hashed_payload.hexdigest()}")
    current_time = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_type = "application/json; charset=utf-8"
    request_uri = f"/api/v3/transaction/{api_key}/debit"
    message = (
        "POST"
        + "\n"
        + hashed_payload.hexdigest()
        + "\n"
        + content_type
        + "\n"
        + current_time
        + "\n"
        + request_uri
    )
    sig = base64.b64encode(
        hmac.new(
            shared_secret.encode(),
            msg=message.encode(),
            digestmod=hashlib.sha512,
        ).digest()
    ).decode()
    logging.debug(f"Concatenated message: \n{message}")
    logging.info(f"Signature: {sig}")
    return current_time, sig, shrinked_payload


def debit_with_signature(merchant_txn_id):
    url = f"{base_url}/transaction/{api_key}/debit"
    user_pass = f"{api_username}:{api_password}"
    encoded_user_pass = base64.b64encode(user_pass.encode()).decode()
    (current_time, sig, payload) = generate_signature(merchant_txn_id)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {encoded_user_pass}",
        "X-Signature": sig,
        "Date": current_time,
    }
    logging.debug(f"URL: {url}")
    logging.debug(f"Headers: \n{headers}")
    logging.debug(f"Payload: \n{payload}")
    resp = requests.post(url=url, headers=headers, data=payload)
    logging.debug(f"Response status: {resp.status_code}")
    logging.debug(f"Response: {resp.text}")
    try:
        logging.info(
            "Redirect URL: " + resp.json()["redirectUrl"].replace("\\", "")
        )
    except KeyError:
        logging.warning(
            "The result is not as expected. Please change the logging level to"
            " debug."
        )

debit_with_signature("Test2-18052022")