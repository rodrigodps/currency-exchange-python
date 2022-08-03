import json
from datetime import datetime

import requests


def exchange(source, target, mock=False):
    if mock:
        d = datetime.now()
        return {'success': True,
                'timestamp': d.timestamp(),
                'base': source,
                'date': d.date(),
                'rates': {target: 4.5}
                }
    else:
        url = f'https://api.apilayer.com/exchangerates_data/latest?symbols={target}&base={source}'

        payload = {}
        headers = {
            "apikey": "HJ0JAiAqmPlcCwkWRVdeKNFCG54eTirB"
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=30)

        # status_code = response.status_code
        return json.loads(response.text)
