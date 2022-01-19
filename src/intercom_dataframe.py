from math import ceil
from time import time

import pandas as pd
from google.cloud import bigquery

from intercom.intercom_loader import IntercomLoader
from intercom.intercom_data import IntercomData
from utils.helperutils import HelperUtils
from bigquery import BigQueryHelper


def get_intercom_companies_dataframe(intercom_config):
    page = 1
    intercom_loader = IntercomLoader()
    intercom_data = IntercomData()

    # Load first batch of companies
    raw_companies = intercom_loader.get_companies(page)

    # Start paginated parsing and loading
    while page < intercom_loader.total_pages_for_companies:

        # Iterate over each company item
        for raw_company in raw_companies:

            # Iterate over each tag within a company
            for raw_tag in raw_company.tags[intercom_config['tag_id']]:
                # Add company to intercom_data collection
                intercom_data.add_company(raw_company, raw_tag)

        # Move to next page
        page += 1

        # Load next batch of companies
        raw_companies = intercom_loader.get_companies(page)

    return pd.DataFrame(intercom_data.get_companies())


def get_intercom_contacts_dataframe(intercom_config):
    intercom_loader = IntercomLoader()
    intercom_data = IntercomData()

    # Start paginated parsing and loading
    while True:

        raw_contacts = intercom_loader.get_contacts()
        # Iterate over each company item
        for raw_contact in raw_contacts:

            intercom_data.add_contact(raw_contact)

        # Check if there are more pages
        if intercom_loader.has_more_contacts() != True:
            break

    return pd.DataFrame(intercom_data.get_contacts())


def get_intercom_contact_companies_dataframe(intercom_config):
    intercom_loader = IntercomLoader()
    intercom_data = IntercomData()

    # Start paginated parsing and loading
    while True:
        raw_contacts = intercom_loader.get_contacts()

        # Iterate over each contact item
        for raw_contact in raw_contacts:
            intercom_data.add_contact(raw_contact)

            # Iterate over each company within a contact
            company_count = raw_contact.companies.total_count
            if company_count != 0:
                # Check if total companies are 10 or less.
                if company_count <= 10:
                    for raw_contact_company in raw_contact.companies.get('data'):
                        # Add company to intercom_data collection
                        intercom_data.add_contact_company(
                            raw_contact, raw_contact_company)
                else:

                    raw_contact_companies = intercom_loader.get_contact_companies(
                        raw_contact.id)
                    for raw_contact_company in raw_contact_companies:
                        # Add contact_id and company_id to intercom_data collection
                        intercom_data.add_contact_company(
                            raw_contact, raw_contact_company)

        if intercom_loader.has_more_contacts() != True:
            break

    return pd.DataFrame(intercom_data.get_contact_companies())


def load_intercom_companies_dataframe(bq_config, dataframe):
    bq_helper = BigQueryHelper(
        bq_config['intercom_company_table_id'], bigquery.LoadJobConfig(schema=[
            # Specify the type of columns whose type cannot be auto-detected.
            # For example the "company_id" column uses pandas dtype "object", so its
            # data type is ambiguous.
            bigquery.SchemaField(
                "company_id", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField(
                "last_request_at", bigquery.enums.SqlTypeNames.INT64),
            bigquery.SchemaField(
                "id", bigquery.enums.SqlTypeNames.STRING)
        ],
            write_disposition=bq_config['intercom_company_write_deposition']))

    bq_helper.load_table(dataframe)
    table = bq_helper.get_table()
    print(
        f"Intercom Companies => Loaded {table.num_rows} rows with {len(table.schema)} columns to {bq_helper.table_id}"
    )
    bq_helper.close_client()


def load_intercom_contact_dataframe(bq_config, dataframe):
    bq_helper = BigQueryHelper(
        bq_config['intercom_contact_table_id'], bigquery.LoadJobConfig(schema=[
            # Specify the type of columns whose type cannot be auto-detected.
            # For example the "contact_id" column uses pandas dtype "object", so its
            # data type is ambiguous.
            bigquery.SchemaField(
                "contact_id", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField(
                "external_id", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField(
                "name", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField(
                "type", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField(
                "last_seen_at", bigquery.enums.SqlTypeNames.INT64),
            bigquery.SchemaField(
                "signed_up_at", bigquery.enums.SqlTypeNames.INT64),
            bigquery.SchemaField(
                "city", bigquery.enums.SqlTypeNames.STRING)
        ],
            write_disposition=bq_config['intercom_contact_write_deposition']))

    bq_helper.load_table(dataframe)
    table = bq_helper.get_table()
    print(
        f"Intercom Contact => Loaded {table.num_rows} rows with {len(table.schema)} columns to {bq_helper.table_id}"
    )
    bq_helper.close_client()


def load_intercom_contact_companies_dataframe(bq_config, dataframe):
    bq_helper = BigQueryHelper(
        bq_config['intercom_xref_table_id'], bigquery.LoadJobConfig(schema=[
            # Specify the type of columns whose type cannot be auto-detected.
            # For example the "company_id" column uses pandas dtype "object", so its
            # data type is ambiguous.
            bigquery.SchemaField(
                "contact_id", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField(
                "company_id", bigquery.enums.SqlTypeNames.STRING)
        ],
            write_disposition=bq_config['intercom_xref_write_deposition']))

    bq_helper.load_table(dataframe)
    table = bq_helper.get_table()
    print(
        f"Intercom Xref_Contact_Companies => Loaded {table.num_rows} rows with {len(table.schema)} columns to {bq_helper.table_id}"
    )
    bq_helper.close_client()


def intercom_init(event, context):
    utils = HelperUtils()
    bq_config = utils.get_bigquery_config()
    start_time = time()

    # Load Intercom Companies dataframe into BigQuery
    print("Intercom import and load started")
    intercom_companies_dataframe = get_intercom_companies_dataframe(
        utils.get_intercom_config())
    load_intercom_companies_dataframe(bq_config, intercom_companies_dataframe)

    # Load Intercom contacts dataframe into BigQuery
    intercom_contacts_dataframe = get_intercom_contacts_dataframe(
        utils.get_intercom_config())
    load_intercom_contact_dataframe(bq_config, intercom_contacts_dataframe)

    # Load Intercom contact companies dataframe into BigQuery
    intercom_contact_companies_dataframe = get_intercom_contact_companies_dataframe(
        utils.get_intercom_config())
    load_intercom_contact_companies_dataframe(
        bq_config, intercom_contact_companies_dataframe)

    print(f"Intercom => Completed in {ceil(time() - start_time)} seconds")
    return f"Intercom Data Fetch & Load Completed"