# Be sure to run `pip install -r requirements.txt`
# before running this script!
import os

from utils.helperutils import HelperUtils

if HelperUtils.is_production() == False:
    # Change working directory to `src`
    # while in development mode.
    os.chdir(os.path.dirname(__file__))


from jira_dataframe import jira_init
from intercom_dataframe import intercom_init
from hubspot_dataframe import hubspot_init


def jira(event=None, context=None):
    return jira_init(event, context)


def intercom(event=None, context=None):
    return intercom_init(event, context)


def hubspot(event=None, context=None):
    return hubspot_init(event, context)


if HelperUtils.is_production() == False:
    jira(None, None)
    intercom(None, None)
    hubspot(None, None)