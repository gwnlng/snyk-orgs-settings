![Snyk logo](https://snyk.io/style/asset/logo/snyk-print.svg)

![snyk-oss-category](https://github.com/snyk-labs/oss-images/blob/main/oss-community.jpg)

# snyk-orgs-settings
A Snyk Organization model generation

### Description

Generates a JSON extract of Snyk Organizations settings of a Snyk Group. This is the equivalent output JSON after running `orgs:create` command at [snyk-api-import](https://github.com/snyk-tech-services/snyk-api-import#usage).

This will serve as the input to generate a list of import targets for the respective Snyk Organizations at [snyk-api-import](https://github.com/snyk-tech-services/snyk-api-import/blob/master/docs/import-data.md) with `import:data` command.

### Prerequisites

1. Python 3.7 and above
2. Snyk account with SNYK_TOKEN of :heavy_exclamation_mark: **Group Admin** permission

### Installation

Setup Python virtual environment with
```bash
pip3 install -r requirements.txt
```

### Usage

```bash
% export SNYK_TOKEN=<MySnykToken>
% python3 snyk-orgs-settings.py --help
usage: snyk-orgs-settings.py [-h] --group-id GROUP_ID [--orgNameStartsWith ORGNAMESTARTSWITH]

Extracts Snyk Organizations settings

optional arguments:
  -h, --help            show this help message and exit
  --group-id GROUP_ID   The Snyk Group ID found in Group > Settings.
  --orgNameStartsWith ORGNAMESTARTSWITH
                        The Snyk Organization Name found in Organization > Settings. If omitted, process all organizations of Snyk Group token has access to.
% python3 snyk-orgs-settings.py --group-id <MyGroupId> [--orgNameStartsWith <OrgNamePrefix>]
```
### Sample Output

#### snyk-created-orgs.json

```json
{
  "orgData": [
    {
      "id": "09745013-c281-4027-aa7f-0a6985da4802",
      "name": "org2",
      "slug": "org2-1lv",
      "url": "https://app.snyk.io/org/org2-1lv",
      "created": "2022-08-17T02:37:35.137Z",
      "orgId": "09745013-c281-4027-aa7f-0a6985da4912",
      "integrations": {
        "github": "76f73f35-7690-4121-a5a0-b2c279f54c11",
        "bitbucket-cloud": "c8abbdf5-fbec-449a-af25-9927095ecc4c"
      },
      "groupId": "fr0c78bb-6365-462c-8576-e73de8793870"
    }
  ]
}
```

