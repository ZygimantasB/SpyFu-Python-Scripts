import requests
import logging
import base64
import json
from requests.exceptions import RequestException
from typing import Optional
from data import data


class SpyFuAPI:
    def __init__(self, api_url, api_id, secret_key, filename):
        self.api_url = api_url
        self.api_id = api_id
        self.secret_key = secret_key
        self.filename = filename
        self.headers = self.prepare_headers()
        self.all_parameters = self.prepare_all_parameters()

    def get_api_response(self, url: str, headers: dict, params: dict) -> Optional[dict]:
        """
        Send request to spyfu api
        """
        try:
            print(f"Sending request to {url} with parameters {params}")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            print(f"Response received: {response.json()}")
            return response.json()
        except RequestException as error:
            logging.error(f"Request to {url} failed: {error}")
            return None

    def prepare_headers(self) -> dict:
        """
        Prepare headers for spyfu api
        """
        combined = f"{self.api_id}:{self.secret_key}"
        basic_auth = base64.b64encode(combined.encode()).decode()
        headers = {'Authorization': f"Basic {basic_auth}"}
        return headers

    @staticmethod
    def remove_spaces(terms: str) -> str:
        """
        Remove spaces from terms before comma and after comma
        """
        terms_list = terms.split(",")
        cleaned_terms_list = [term.strip() for term in terms_list]
        cleaned_terms = ",".join(cleaned_terms_list)
        return f'"{cleaned_terms}"'

    def prepare_parameters(self, search_criteria: dict) -> dict:
        """
        prepare parameters for spyfu api
        """
        if 'url' in search_criteria and 'terms' in search_criteria:
            cleaned_terms = self.remove_spaces(search_criteria['terms'])
            params = {
                'domain': search_criteria['url'],
                'startingRow': 1,
                'pageSize': 50,
                'countryCode': "UK",
            }
        else:
            print(f"Missing 'url' or 'terms' in search criteria: {search_criteria}")
            params = None

        return params

    def prepare_all_parameters(self):
        """
        Prepare parameters for all search criteria.
        """
        all_search_criteria = data
        all_parameters = [self.prepare_parameters(criteria) for criteria in all_search_criteria if criteria is not None]
        return all_parameters

    def get_spy_fu_data(self):
        """
        Get data from spyfu api
        """
        url_end_point = '/competitors_api/v2/seo/getTopCompetitors'
        url = self.api_url + url_end_point
        all_data = {}
        for params in self.all_parameters:
            response = self.get_api_response(url, self.headers, params)
            data = response['results'] if response else None
            if data is not None:
                json.dumps(data, indent=4)
                all_data[params['domain']] = data
        return all_data
