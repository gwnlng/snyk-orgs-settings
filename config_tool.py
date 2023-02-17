import argparse
import os
import snyk


SNYK_TOKEN = os.getenv("SNYK_TOKEN")
snyk_client = snyk.SnykClient(SNYK_TOKEN, tries=3, delay=1, backoff=2)

def parse_command_line_args():
    """
    Parse command-line arguments
    :return:
    """
    parser = argparse.ArgumentParser(description='Extracts Snyk Organizations settings')
    parser.add_argument(
        "--group-id",
        type=str,
        help="The Snyk Group ID found in Group > Settings.",
        required=True
    )
    parser.add_argument(
        "--orgNameStartsWith",
        type=str,
        help="The Snyk Organization Name found in Organization > Settings. \
            If omitted, process all organizations of Snyk Group token has access to.",
        required=False
    )

    return parser.parse_args()
