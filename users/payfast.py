import urllib.parse
import hashlib
import socket
from werkzeug.urls import url_parse
import requests


def pfValidSignature(pfData, pfParamString):
    # Generate our signature from PayFast parameters
    test_signature = hashlib.md5(pfParamString.encode()).hexdigest()
    print(test_signature)
    print(pfData.get('signature'))
    return pfData.get('signature') == test_signature


def pfValidIP(request):
    valid_hosts = [
        'www.payfast.co.za',
        'sandbox.payfast.co.za',
        'w1w.payfast.co.za',
        'w2w.payfast.co.za',
    ]
    valid_ips = []

    for item in valid_hosts:
        ips = socket.gethostbyname_ex(item)
        if ips:
            for ip in ips:
                if ip:
                    valid_ips.append(ip)
    # Remove duplicates from array
    clean_valid_ips = []
    for item in valid_ips:
        # Iterate through each variable to create one list
        if isinstance(item, list):
            for prop in item:
                if prop not in clean_valid_ips:
                    clean_valid_ips.append(prop)
        else:
            if item not in clean_valid_ips:
                clean_valid_ips.append(item)

    # Security Step 3, check if referrer is valid
    if url_parse(request.headers.get("Referer")).host not in clean_valid_ips:
        return False
    else:
        return True


def pfValidPaymentData(cartTotal, pfData):
    return not (abs(float(cartTotal)) - float(pfData.get('amount_gross'))) > 0.01


def pfValidServerConfirmation(pfParamString, pfHost='sandbox.payfast.co.za'):
    url = f"https://{pfHost}/eng/query/validate"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=pfParamString, headers=headers)
    print(response.text)
    return response.text == 'VALID'


def generateSignature(dataArray, passPhrase):
    payload = ""
    for key in dataArray:
        # Get all the data from PayFast and prepare parameter string
        print(key)
        payload += key + "=" + urllib.parse.quote_plus(dataArray[key].replace("+", " ")) + "&"
    # After looping through, cut the last & or append your passphrase
    # payload = payload[:-1]
    if passPhrase != '':
        payload += f"passphrase={passPhrase}"
    print(payload)
    return hashlib.md5(payload.encode()).hexdigest()
