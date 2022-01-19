BigQuery Loader
This project fetches data from Jira, Intercom and Hubspot instances, parses and transforms data into a dataframe object and then loads it into the data warehouse within Google BigQuery.

Prerequisites
To run the script, you would need Python v3.7.9 or higher installed.

There are certain steps that you need to follow before you can run the project, those are as follows;

The project makes REST calls to Jira, Intercom and Hubspot instances, which requires authentication token to be passed in request header. You need to configure the environment variables beforehand. These variables can either be configured from your Cloud provider's console or by following operating system instructions. Following are the environment variables that project uses;
JIRA_USERNAME: User ID (i.e. email address) of Jira account.
JIRA_TOKEN: Authentication token associated with Jira account.
INTERCOM_TOKEN: Authentication token associated with Intercom account.
HUBSPOT_TOKEN: Authentication token associated with Hubspot account.
Once data is fetched from Jira, Intercom and Hubspot via its respective REST APIs, it is then loaded into Google BigQuery as a dataframe object. Since BigQuery and Google Cloud Functions are in within same project, we don't need to load credentials while executing the functions on GCP. However, when you run the scripts locally, it will require a credentials string (in json format) to be available before data can be loaded within BigQuery. You need to obtain this string from your organization's Google Cloud Platform administrator. Once the string is available, create enivornment variable as BIGQUERY_KEY and set the string as its value. Since the credentials will be in JSON format, be sure to correctly escape the string before setting the variable.
After environment variables are set and private key file is available, install project dependencies by running pip install -r requirements.txt. Please note that if you're running Python 3 along side Python 2, pip command may still be pointing to Python 2, in which case, you would run pip3 install -r requirements.txt.
config.yml
The config.yml file keeps configuration that project primarily relies on, refer to the inline comments for each property within this file to understand what it does.

How to run?
Once all the steps as mentioned in prerequisites section are done, run the project by running python main.py.