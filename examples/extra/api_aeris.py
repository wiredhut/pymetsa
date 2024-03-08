# import sys
# sys.path.append("/Users/denis/Downloads/pymetsa/")

import os
from pathlib import Path
from datetime import datetime

from pymetsa.download.from_aeris import locations_loop


client_id = os.getenv('AERIS_CLIENT_ID')
client_secret = os.getenv('AERIS_CLIENT_SECRET')

request_fields = [
    'place.name',
    'place.country',
    'periods.tempF',
    'periods.feelslikeF',
    'periods.humidity',
]

location_list = [
    "minneapolis,mn",
    "43.67,-70.26",
    "80452",
    "berkley,uk"
]


if __name__=="__main__":
    full_df = locations_loop(locations=location_list, custom_fields=request_fields)

    now = datetime.now()
    output_dir = Path('aeris_output')
    output_dir.mkdir(exist_ok=True)

    download_location = output_dir / f"conditions-download-{now.strftime('%Y-%m-%dT%H:%M')}.csv"
    full_df.to_csv(download_location, encoding="utf-8")

