# USAA-Assemblyline4 Admin Guide

## Configuration

USAA-Assemblyline4 requires an Assemblyline 4 instance and API creds.

### Setting API creds for global use

To set-up global API creds:

```text
> al4.setup.apicreds userid apikey
```

### Setting API creds for each user

A user may set-up their own API creds:

```text
> al4.setup.apicreds --self userid apikey
```

### Setting the API Endpoint for global use

To configure a global API endpoint:

```text
> al4.setup.apihost https://al.local:443
```

### Setting the http traffic proxy

Configure a proxy specific for Assemblyline:

```text
> al4.setup.proxy socks5://yourproxyhost:8888
```

or

Disable the use of any proxy, including the use of any proxies configured in the Cortex:

```text
> al4.setup.proxy --disable
```

### Permissions

#### User Roles

```text
Package (usaa-assemblyline4) defines the following permissions:
power-ups.al4.user              : Controls user access to USAA-Assemblyline4.
power-ups.al4.admin             : Controls access to all setup commands except al4.setup.apicreds
```

An admin will need to be a member of both the `power-ups.al4.user` and `.admin` groups to use this Power-Up.

You may add rules to users/roles directly from storm:

```text
> auth.user.addrule analyst power-ups.al4.user
User (analyst) added rule: power-ups.al4.user

or:

> auth.role.addrule admins power-ups.al4.admin
Role (admins) added rule: power-ups.al4.admin
```

#### Cortex Permissions

A user must have the following cortex permissions.

```text
node.add
node.prop.set
node.edge.add
node.tag.add
```

#### Assemblyline 4 Roles

When creating an API key within Assemblyline 4, the following roles must be selected at a minimum.

```text
File Download
File Detail
Submission Create
Submission View
```

## Exported APIs

USAA-Assemblyline4 provides the following exported APIs.

### al4.searchIndex

```text
Module: al4
function: searchIndex

    Search a specific Assemblyline 4 datastore index.

    Note: This will gather all results and return them all at once.

    Parameters:
        searchQuery (str): AL Search Query
        index (str): AL Index. e.g. submission
        maxResults (int): Max number of results per page
        fields (str): Comma separate list of fields to return. e.g. "id,score"
        sort (str): How to sort the results. e.g. field asc

    Returns:
        list of results (list): List of AL Search Results. The actual results and not the metadata about the search.
            e.g. This is a result item from a submission index search.
                {
                    "archived": false,
                    "classification": "TLP:WHITE",
                    "error_count": 0,
                    "file_count": 4,
                    "from_archive": false,
                    "id": "53tGo4lBhjr2l0s5CY8sa1",
                    "max_score": 13,
                    "params": {
                        "description": "Inspection of URL: https://foo.local",
                        "submitter": "admin"
                    },
                    "sid": "53tGo4lBhjr2l0s5CY8sa1",
                    "state": "completed",
                    "times": {
                        "submitted": "2023-04-21T14:57:48.697835Z"
                    },
                    "to_be_deleted": false
                },
```

## Node Actions

USAA-Assemblyline4 provides the following node actions in Optic:

```text
Name : al4.file.download
Desc : Download a file from Assemblyline.
Forms: file:bytes, hash:sha256

Name : al4.file.enrich
Desc : Enrich the specified file with all the latest analytic service results from Assemblyline 4.
Forms: file:bytes, hash:sha256

Name : al4.file.submit
Desc : Submit the specified file to Assemblyline for analysis and wait for the results.
Forms: file:bytes

Name : al4.url.submit
Desc : Submit the specified URL to Assemblyline for analysis and wait for the results.
Forms: inet:url
```

## Onload Events

USAA-Assemblyline4 extends the model by adding the `_assemblyline:type` property to `file:bytes` nodes.
