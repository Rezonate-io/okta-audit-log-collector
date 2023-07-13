import requests
from datetime import datetime, timedelta
import time
import json


def get_okta_audit_logs(api_key, start_date, end_date,your_okta_domain):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {api_key}',
    }

    date_format = '%Y-%m-%dT%H:%M:%S.000Z'

    start_date_str = datetime.strptime(start_date, '%Y-%m-%d').strftime(date_format)
    end_date_str = datetime.strptime(end_date, '%Y-%m-%d').strftime(date_format)

    all_data = []
    base_url = f'https://{your_okta_domain}/api/v1/logs?since={start_date_str}&until={end_date_str}&limit=100'

    while True: 
        response = requests.get(base_url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f'Error with status code: {response.status_code}')

        data = response.json()
        if not data:
            break
        
        with open('results.txt', 'a') as fp:
            fp.write(
                '[' +
                ',\n'.join(json.dumps(i) for i in data) +
                ']\n')


        # Wait for a second to avoid hitting API rate limits
        time.sleep(1)
        
        if response.links and 'next' in  response.links:
            next_url = response.links['next']['url']
        else: 
            print("finished")
            break
        print(next_url)
        base_url = next_url
        

    return all_data

def main():
    print("Okta Audit Log Collector")
    print("--------------------------")
    api_key = input('Enter your API Key: ')
    start_date = input('Enter the start date in format YYYY-MM-DD: ')
    end_date = input('Enter the end date in format YYYY-MM-DD: ')
    your_okta_domain = input('Enter your okta domain (rezonate.okta.com):')

    get_okta_audit_logs(api_key, start_date, end_date,your_okta_domain)


if __name__ == "__main__":
    main()
