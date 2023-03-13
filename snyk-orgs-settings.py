import json
import os
import config_tool
import snyk
import sys


def dump_orgs_data(group_id, orgs, mapping_json=None, map_attribute=None, snyk_org_key=None, scm_org_key=None):
    """
    Dumps out json orgs format data for api-import
    :param group_id: Snyk Group ID
    :param orgs: Snyk organizations (list)
    :param mapping_json: name mapping dictionary
    :param map_attribute: attribute to mapping list
    :param snyk_org_key: Snyk organization name key
    :param scm_org_key: SCM org name key
    :return: org name
    """
    json_data = {}
    try:
        mapped_names = {}
        if mapping_json is not None:
            with open(mapping_json, 'r') as fp:
                mapped_names = json.load(fp)

        for org in orgs:
            org_id = org['id']
            org['orgId'] = org_id
            # map it to the SCM organization scoped name if provided
            org['name'] = get_scm_org_name(org['name'], mapped_names, map_attribute, snyk_org_key,
                                           scm_org_key) if mapped_names else org['name']

            print(f"calling org/{org_id}/integrations API...")
            resp = config_tool.snyk_client.get(f"org/{org_id}/integrations")
            if resp.status_code != 200:
                raise snyk.errors.SnykHTTPError(resp.reason)

            integrations = json.loads(resp.text)
            org['integrations'] = integrations
            org['groupId'] = group_id
    except snyk.errors.SnykHTTPError as snyk_err:
        print(f"Error encountered with Snyk API /integrations: {str(snyk_err)}")
    except KeyError as key_err:
        print(f"Error encountered retrieving mapping attribute from json: {str(key_err)}")
    except ValueError as val_err:
        print(f"Error encountered at names mapping keys: {str(val_err)}")
    except (FileNotFoundError, json.decoder.JSONDecodeError) as fp_err:
        print(f"Error loading SCM mapping json file: {str(fp_err)}")

    json_data['orgData'] = orgs
    with open("snyk-created-orgs.json", "w") as fp:
        json.dump(json_data, fp, indent=2)

    print("Exported snyk-created-orgs.json")


def get_scm_org_name(org_name, mapping, map_attribute, snyk_org_key, scm_org_key):
    """
    Gets the mapped SCM organizational-scoped name e.g. Bitbucket server project name, GHE org name
    :param org_name: Snyk Org name
    :param mapping: names mapping dict
    :param map_attribute: attribute to list of mapped names
    :param snyk_org_key: key to snyk org name value
    :param scm_org_key: key to scm org name value
    :return: scm_org_name
    """
    matched_org_names = [x[scm_org_key] for x in mapping[map_attribute] if x[snyk_org_key] == org_name]
    # only a 1:1 mapping supported so just retrieve its first
    scm_org_name = matched_org_names[0] if matched_org_names else org_name
    return scm_org_name


# https://snyk.docs.apiary.io/#reference/groups/list-all-organizations-in-a-group/list-all-organizations-in-a-group
def list_all_orgs(group_id, org_name=None, per_page=100):
    """
    List all Snyk organizations in a Snyk group from snyk api query and response
    :param group_id: group id (string)
    :param org_name: organization name starting with this value case-insensitive (str)
    :param per_page: The number of results to return (maximum is 100) (int)
    :return: org_ids (list)
    """
    orgs = []
    page_num = 1
    name_param = f"&name={org_name}" if org_name else ""
    try:
        print(f"calling page {page_num} at group/{group_id}/orgs API...")
        resp = config_tool.snyk_client.get(f"group/{group_id}/orgs?perPage={per_page}&page={page_num}{name_param}")
        if resp.status_code != 200:
            raise snyk.errors.SnykHTTPError(resp.reason)
        resp_body = json.loads(resp.text)
        orgs_list = resp_body['orgs']

        # see link above for response body to paginated request
        while orgs_list:
            # extract orgs attribute from json
            orgs.extend(orgs_list)
            page_num += 1
            print(f"calling page {page_num} at group/{group_id}/orgs API...")
            resp = config_tool.snyk_client.get(f"group/{group_id}/orgs?perPage={per_page}&page={page_num}{name_param}")
            if resp.status_code != 200:
                raise snyk.errors.SnykHTTPError(resp.reason)
            resp_body = json.loads(resp.text)
            orgs_list = resp_body['orgs']
    except snyk.errors.SnykHTTPError as snyk_err:
        print(f"Error encountered with Snyk API /orgs: {str(snyk_err)}")

    return orgs


def generate_orgs_data(cli_arguments):
    """
    Generates orgs data for api-import
    :param cli_arguments: CLI arguments (Namespace)
    :return:
    """
    # dump orgsData json map required at snyk-api-import step 4
    orgs = list_all_orgs(cli_arguments.group_id, org_name=cli_arguments.orgNameStartsWith)
    dump_orgs_data(cli_arguments.group_id, orgs, mapping_json=cli_arguments.mapping_json,
                   map_attribute=cli_arguments.map_attribute, snyk_org_key=cli_arguments.snyk_org_key,
                   scm_org_key=cli_arguments.scm_org_key)


if __name__ == '__main__':
    if not os.getenv("SNYK_TOKEN"):
        print("token not set at $SNYK_TOKEN")
        sys.exit(1)

    # parse the arguments
    cli_args = config_tool.parse_command_line_args()
    print(cli_args)
    if cli_args.mapping_json is not None and (
            cli_args.map_attribute is None or cli_args.snyk_org_key is None or cli_args.scm_org_key is None):
        print(f"Mapping and key arguments are not all set")
        sys.exit(1)

    generate_orgs_data(cli_args)
