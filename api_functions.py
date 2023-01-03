import json

import pandas as pd
import requests
from pandas import json_normalize
from settings import api_exchange_address


def get_book_summary_by_currency(currency, kind):
    url = "/api/v2/public/get_book_summary_by_currency"
    parameters = {'currency': currency,
                  'kind': kind}
    # send HTTPS GET request
    json_response = requests.get((api_exchange_address + url + "?"), params=parameters)
    response_dict = json.loads(json_response.content)
    # print(json_response.content)
    instrument_details = response_dict["result"]
    pd.set_option('display.max_rows', None)
    print(json_normalize(instrument_details))


    return instrument_details
