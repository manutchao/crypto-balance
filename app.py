""" Script to interrogate crypto wallet"""

import os

import requests
from coinbase.rest import RESTClient as CoinbaseClient

try:
    API_KEY_COINBASE = os.environ["API_KEY_COINBASE"]
except KeyError:
    print("Environment variable 'API_KEY_COINBASE' not found")
    API_KEY_COINBASE = None

try:
    API_SECRET_COINBASE = os.environ["API_SECRET_COINBASE"]
except KeyError:
    print("Environment variable 'API_SECRET_COINBASE' not found")
    API_SECRET_COINBASE = None


client_coinbase = CoinbaseClient(
    api_key=API_KEY_COINBASE, api_secret=API_SECRET_COINBASE
)

accounts_coinbase = client_coinbase.get_accounts()

content_wallet_coinbase = [
    [
        account["available_balance"]["currency"],
        account["available_balance"]["value"],
        account["available_balance"]["currency"] + "-EUR",
    ]
    for account in accounts_coinbase["accounts"]
    if float(account["available_balance"]["value"]) > float(0)
]


print("CRYPTO" + "\t\t" + "PRIX UNIT" + "\t\t" + "QUANTITE" + "\t\t" + "MONTANT TOTAL")

MONTANT_TOTAL_COINBASE = 0
for asset in content_wallet_coinbase:
    URL = "https://api.coinbase.com/v2/prices/" + asset[2] + "/spot"
    requestResponse = requests.get(URL)
    parsedJSONResponse = requestResponse.json()
    MONTANT_TOTAL_COINBASE += float(parsedJSONResponse["data"]["amount"]) * float(
        asset[1]
    )
    DEVISE = "€"
    print(
        parsedJSONResponse["data"]["base"]
        + "\t\t"
        + str(round(float(parsedJSONResponse["data"]["amount"]), 4))
        + "\t\t"
        + str(round(float(asset[1]), 4))
        + "\t\t"
        + str(round(float(parsedJSONResponse["data"]["amount"]) * float(asset[1]), 4))
        + DEVISE
    )
print()
print("TOTAL COINBASE" + "\t\t" + str(round(MONTANT_TOTAL_COINBASE, 3)) + DEVISE)
