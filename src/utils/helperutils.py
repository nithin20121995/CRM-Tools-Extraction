import os

import yaml as yml


class HelperUtils:
    def __init__(self):
        self.config_file = "config.yml"

    @staticmethod
    def is_production():
        return os.environ.get('PRODUCTION', 'False') == 'True'

    def get_jira_config(self):
        with open(self.config_file, "r") as f:
            return yml.safe_load(f)['jira']

    def get_intercom_config(self):
        with open(self.config_file, "r") as f:
            return yml.safe_load(f)['intercom']

    def get_hubspot_config(self):
        with open(self.config_file, "r") as f:
            return yml.safe_load(f)['hubspot']

    def get_bigquery_config(self):
        with open(self.config_file, "r") as f:
            return yml.safe_load(f)['big_query']

    def get_network_config(self):
        with open(self.config_file, "r") as f:
            return yml.safe_load(f)['network']

    def get_jira_auth_username(self):
        return os.environ.get('JIRA_USERNAME', None)

    def get_jira_auth_token(self):
        return os.environ.get('JIRA_TOKEN', None)

    def get_intercom_token(self):
        return os.environ.get('INTERCOM_TOKEN', None)

    def get_hubspot_token(self):
        return os.environ.get('HUBSPOT_TOKEN', None)

    def get_bigquery_key(self):
        return os.environ.get('BIGQUERY_KEY', None)

    def get_list_of_batches(self, source_list, batch_size):
        batches = []
        batch = []
        source_list_len = len(source_list)
        for i in range(source_list_len):
            batch.append(source_list[i])
            if (len(batch) == batch_size or i == source_list_len - 1):
                batches.append(batch)
                batch = []

        return batches