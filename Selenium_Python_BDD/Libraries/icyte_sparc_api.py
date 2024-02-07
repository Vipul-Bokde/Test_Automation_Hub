import os
import logging
import requests
from datetime import datetime

LOGGER = logging.getLogger(__name__)


class IcyteSparcApi:
    evidences_path = "./evidences"

    def __init__(self, domain):
        self.domain = domain
        self.headers = {"content-type": "application/json"}
        self.cookies = {}

    # common requests

    def login(self, username, password):
        data = {"username": username, "password": password}
        response = requests.post("{}/api/auth/login/".format(self.domain), json=data, headers=self.headers)
        LOGGER.info("Login response {}".format(response.status_code))
        token = response.text
        self.cookies = {'currentUser': token}

    def list_service_client(self):
        response = requests.get("{}/api/auth/user/218/clients/services/".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("List clients response {}".format(response.status_code))
        return response.json()

    def get_client_by(self, client_name, service_name):
        services = self.list_service_client()
        for service in services:
            if service["client_name"] == client_name and service["service_name"] == service_name:
                return service
        return None

    def choose_services(self, contract):
        response = requests.post("{}/api/auth/environment/".format(self.domain), json=contract, headers=self.headers,
                                 cookies=self.cookies)
        LOGGER.info("Choose services response {}".format(response.status_code))
        token = response.text
        self.cookies = {'currentUser': token}

    def get_pricing(self):
        response = requests.get("{}/api/common/pricings/".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("Pricing response {}".format(response.status_code))
        return response.json()

    def get_approvals(self):
        response = requests.get("{}/api/common/approvals/?client=&diff_type=".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("Approvals response {}".format(response.status_code))
        return response.json()

    def get_contracts_client(self):
        response = requests.get("{}/api/common/contractclientcustomers/".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("List contract client response {}".format(response.status_code))
        return response.json()

    def get_products(self):
        response = requests.get("{}/api/common/products/".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("Products response {}".format(response.status_code))
        return response.json()

    def logout(self):
        response = requests.get("{}/api/auth/logout".format(self.domain), cookies=self.cookies, headers=self.headers)
        LOGGER.info("Logout response {}".format(response.status_code))

    # Medicaid requests

    def get_medi_invoices(self):
        response = requests.get("{}/api/medicaid/invoices/?settled=1".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("List Medicaid invoices response {}".format(response.status_code))
        return response.json()

    def get_states(self):
        response = requests.get("{}/api/medicaid/states".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("List states response {}".format(response.status_code))
        return response.json()

    def search_state_by_id(self, id):
        states = self.get_states()
        for state in states:
            if state["id"] == id:
                return state
        return None

    def get_programs(self):
        response = requests.get("{}/api/medicaid/programs".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("List programs response {}".format(response.status_code))
        return response.json()

    def get_state_associated_programs(self):
        response = requests.get("{}/api/medicaid/program/entities/available".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("Available response {}".format(response.status_code))
        return response.json()

    def get_postmarks(self):
        response = requests.get("{}/api/medicaid/postmarks".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("Postmark response {}".format(response.status_code))
        return response.json()

    def payment_tracker(self, filter_tracker):
        response = requests.post("{}/api/medicaid/payment_tracker/view/".format(self.domain), json=filter_tracker,
                                 headers=self.headers, cookies=self.cookies)
        LOGGER.info("Payment Tracker response {}".format(response.status_code))
        return response.json()

    def download_file(self, file_id, file_name):
        response = requests.get("{}/api/medicaid/invoice/file/{}/".format(self.domain, file_id), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("Download file response {}".format(response.status_code))
        date_time_obj = datetime.now()
        timestamp_str = date_time_obj.strftime("%d%m%Y_%H%M%S")
        if not os.path.exists(IcyteSparcApi.evidences_path):
            os.makedirs(IcyteSparcApi.evidences_path)
        file = open(IcyteSparcApi.evidences_path + "/{}_{}".format(timestamp_str, file_name), 'wb')
        file.write(response.content)
        file.close()

    # UBR requests

    def get_ubr_invoices(self):
        response = requests.get("{}/api/mc/invoices/?settled=1".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("List UBR invoices response {}".format(response.status_code))
        return response.json()

    def get_contracts(self):
        response = requests.get("{}/api/mc/contractheaders/".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("List UBR contracts response {}".format(response.status_code))
        return response.json()

    def get_rebates_condition_option(self):
        response = requests.get("{}/api/mc/conditions/All".format(self.domain), cookies=self.cookies,
                                headers=self.headers)
        LOGGER.info("List UBR rebate condition option response {}".format(response.status_code))
        return response.json()
