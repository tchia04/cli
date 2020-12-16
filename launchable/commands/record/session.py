import click
import os

from ...utils.http_client import LaunchableClient
from ...utils.token import parse_token
from ...utils.env_keys import REPORT_ERROR_KEY


@click.command()
@click.option(
    '--name',
    'build_name',
    help='build identifier',
    required=True,
    type=str,
    metavar='BUILD_ID'
)
def session(build_name):
    token, org, workspace = parse_token()

    headers = {
        "Content-Type": "application/json",
    }

    client = LaunchableClient(token)

    try:
        session_path = "/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions".format(
            org, workspace, build_name)
        res = client.request("post", session_path, headers=headers)
        res.raise_for_status()
        session_id = res.json()['id']

        click.echo(session_id)
        return session_id

    except Exception as e:
        if os.getenv(REPORT_ERROR_KEY):
            raise e
        else:
            click.echo(e, err=True)
