import json
import requests
import sys
import os
from dateutil import parser
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import validators
import re


def post_message_slack(message: str):
    """
    Post a message to the Slack channel provided.
    """
    channel_id = os.environ['SLACK_CHANNEL_ID']
    slack_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    try:
        result = slack_client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        print(result)

    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")


def parse_version_details(version_details_raw: str) -> (str, str):
    """
    Return tuple containing the version and date of a release.
    """
    version_raw = version_details_raw.strip().split()
    rel_date_raw = version_details_raw.strip().split("(")
    rel_version = version_raw[1]
    print(rel_date_raw)
    rel_date_ = rel_date_raw[1].strip(")")

    # Removing the comma so we can convert this string date into a datetime object
    release_date_clean = rel_date_.replace(",", "")

    return rel_version, release_date_clean


if __name__ == '__main__':
    url = sys.argv[1]
    validate_url = validators.url(url)

    if not validate_url:
        print("Invalid URL provided!")
        sys.exit(1)

    response = requests.get(url)
    with open("release-notes.txt", "w") as f:
        f.write(response.text)
        f.close()

    releases_file = open("release-notes.txt", "r")
    count = 0
    versions = []
    dates = {}
    bc_dict = {}
    latest_release_details = []

    while True:
        breaking_changes = []
        line = releases_file.readline()
        if line.strip().startswith("##"):
            if not re.search("Previous Releases", line):
                version, release_date_raw = parse_version_details(line)
                versions.append(version)
                if release_date_raw != "Unreleased":
                    release_date = parser.parse(release_date_raw)
                    date_today = datetime.today()
                    if date_today <= release_date:
                        latest_release_details[0] = version
                        latest_release_details[1] = release_date
                dates[version] = release_date_raw
                count += 1

        if line.strip() == "BREAKING CHANGES:":
            line = releases_file.readline()
            while line.strip().startswith("*"):
                breaking_changes.append(line.strip())
                line = releases_file.readline()
            bc_dict[versions[count - 1]] = breaking_changes

        if not line:
            print(json.dumps(bc_dict, sort_keys=True, indent=4))
            print(dates)
            break

    releases_file.close()
