import os
import json
import time
from requests import request
from typing import List

import pandas as pd

# sample url for current conditions
# http://api.aerisapi.com/conditions/55343?client_id=[CLIENT_ID]&client_secret=[CLIENT_SECRET]

client_id = os.getenv('AERIS_CLIENT_ID')
client_secret = os.getenv('AERIS_CLIENT_SECRET')


def aeris_api_dataframe(location: str, custom_fields: List[str] = None):
    formatted_fields = []
    if custom_fields is not None:
        formatted_fields = ','.join(custom_fields)

    print(f"retrieving data for {location}...")
    res = request(
        method="GET",
        url=f"https://api.aerisapi.com/conditions/{location}",
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "fields": formatted_fields,
        }
    )
    
    if res.status_code != 200:
        raise Exception(f"status code was not 200: {res.status_code}")
    
    api_response_body = json.loads(res.text)

    try:
        df_pre_period = pd.json_normalize(api_response_body['response'][0]).drop("periods", axis=1)
        df_periods = pd.json_normalize(api_response_body['response'][0], "periods", record_prefix="periods.")

        return df_pre_period.join(df_periods, how="cross")
    except IndexError:
        print(f"API Response did not contain periods. Verify request parameters are correct.\n\nRequest:\n{res.url}\n\nResponse:\n{api_response_body}")


def locations_loop(locations: List, custom_fields: List):
    all_locs = []

    for loc in locations:
        all_locs.append(aeris_api_dataframe(location=loc, custom_fields=custom_fields))
        time.sleep(3)

    return pd.concat(all_locs, ignore_index=True)
