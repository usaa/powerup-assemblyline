# Storm Package: usaa-assemblyline4

## Storm Commands

This package implements the following Storm Commands.

### al4.file.download

```text
Download a file from Assemblyline.

This command takes a file:bytes or hash:sha256 node as input and downloads the corresponding file from
Assemblyline into the axon.

Examples:

    // Download a file into the axon
    file:bytes=5e52777a11d9b4728ae499a3437abaa8b3acefa1699f2928a4f02aa3e8f213e3 | al4.file.download

    // Download a file from a hash:sha256 node and pivot to file:bytes node
    hash:sha256=5e52777a11d9b4728ae499a3437abaa8b3acefa1699f2928a4f02aa3e8f213e3 | al4.file.download | -> file:bytes

Usage: al4.file.download [options]

Options:

  --help                      : Display the command usage.
  --debug                     : Show verbose debug output.
  --yield                     : Yield the newly created nodes.

Inputs:

    file:bytes
    hash:sha256
```

### al4.file.enrich

```text
Enrich the specified file with all the latest analytic service results from Assemblyline 4.

Examples:

    // Enrich the specified file
    file:bytes=5e52777a11d9b4728ae499a3437abaa8b3acefa1699f2928a4f02aa3e8f213e3 | al4.file.enrich

    // Enrich the specified file and yield the resulting nodes.
    hash:sha256=5e52777a11d9b4728ae499a3437abaa8b3acefa1699f2928a4f02aa3e8f213e3 | al4.file.enrich --yield

Usage: al4.file.enrich [options]

Options:

  --help                      : Display the command usage.
  --debug                     : Show verbose debug output.
  --yield                     : Yield the newly created nodes.
  --asof <asof>               : Specify the maximum age for a cached result. To disable caching, use --asof now. (default: -30days)

Inputs:

    file:bytes
    hash:sha256
```

### al4.file.submit

```text
Submit the specified file to Assemblyline for analysis and wait for the results.

The file must be present in the axon.

The AL submission parameters used are based on the associated Assemblyline account.

Examples:

    // Submit files tagged with #mal to Assemblyline for analysis
    file:bytes#mal | al4.file.submit

    // Use the --force flag to ignore the Assemblyline analysis results cache and force a re-analysis of the file
    file:bytes#mal | al4.file.submit --force

    // Do not wait for the analysis to complete
    file:bytes#mal | al4.file.submit --nowait

Usage: al4.file.submit [options]

Options:

  --help                      : Display the command usage.
  --debug                     : Show verbose debug output.
  --yield                     : Yield the newly created nodes.
  --force                     : Ignore Assemblyline results cache and force a re-scan.
  --nowait                    : Do not wait for analysis results.

Inputs:

    file:bytes - Any file:bytes present in the axon.
```

### al4.setup.apicreds

```text
Set the Assemblyline API user and key.

Permissions: Requires power-ups.al4.admin for setting API creds for all users.

Examples:
    // Set for all users
    al4.setup.apicreds <apiuser> <apikey>

    // Set for yourself only
    al4.setup.apicreds --self <apiuser> <apikey>

Usage: al4.setup.apicreds [options] <apiuser> <apikey>

Options:

  --help                      : Display the command usage.
  --self                      : Set the key as a user variable. If not used, it will be set globally.
  --show-scope                : Show the currently configured API key's scope.
  --show-creds                : Show the currently configured API creds.
  --remove                    : Remove the currently configured API creds.

Arguments:

  [apiuser]                   : Assemblyline API User
  [apikey]                    : Assemblyline API Key
```

### al4.setup.apihost

```text
Set the Assemblyline API host endpoint.

Permissions: Requires power-ups.al4.admin.

Examples:

    // Set for all users
    al4.setup.apihost https://al.local:443

Usage: al4.setup.apihost [options] <apihost>

Options:

  --help                      : Display the command usage.
  --show                      : Show the currently configured API Host.

Arguments:

  [apihost]                   : Assemblyline API Host Endpoint
```

### al4.setup.proxy

```text
Manage where the Assemblyline Power-Up proxies http traffic to.

Permissions: Requires power-ups.al4.admin.

Examples:

  // Set a new proxy URL that only affects the Assemblyline Power-Up
  al4.setup.proxy socks5://yourproxyhost:8888

  // Remove the configured Assemblyline proxy and accept the system default proxy
  al4.setup.proxy --remove

  // Disable the use of any proxy, including the use of any proxies configured in the Cortex
  al4.setup.proxy --disable

Usage: al4.setup.proxy [options] <proxy>

Options:

  --help                      : Display the command usage.
  --show-proxy                : Show the currently configured proxy value.
  --disable                   : Disable the use of any proxy, including the use of any proxies configured in the Cortex.
  --remove                    : Reset the configured proxy and accept the system default proxy.

Arguments:

  [proxy]                     : A URL to proxy requests to.
```

### al4.setup.tagprefix

```text
Set the tag prefix when recording Assemblyline tags.

If not specified, the default tag prefix is: rep.assemblyline

Any characters in the Assemblyline tag values incompatible with Synapse tag names are replaced with "_".

Permissions: Requires power-ups.al4.admin.

Usage: al4.setup.tagprefix [options] <tag>

Options:

  --help                      : Display the command usage.
  --show                      : Show the currently configured tag prefix.

Arguments:

  [tag]                       : The tag prefix to use.
```

### al4.submission.enrich

```text

Retrieve the analysis results for a given Assemblyline submission and enrich the corresponding nodes.

Examples:

    // Retrieve the Assemblyline analysis results for a given submission
    al4.submission.enrich 44A8cH7F03NSF6qqOWOktq

    // Retrieve the Assemblyline analysis results for a given submission ignoring any local Synapse cache
    al4.submission.enrich 44A8cH7F03NSF6qqOWOktq --asof now

Usage: al4.submission.enrich [options] <submission_id>

Options:

  --help                      : Display the command usage.
  --debug                     : Show verbose debug output.
  --yield                     : Yield the newly created nodes.
  --asof <asof>               : Specify the maximum age for a cached result. To disable caching, use --asof now. (default: -30days)

Arguments:

  <submission_id>             : The Assemblyline submission id to model analysis results from.
```

### al4.url.submit

```text
Submit the specified URL to Assemblyline for analysis and wait for the results.

The AL submission parameters used are based on the associated Assemblyline account.

Examples:

    // Submit URLs tagged with #mal to Assemblyline for analysis
    inet:url#mal | al4.url.submit

    // Use the --force flag to ignore the Assemblyline analysis results cache and force a re-analysis of the URL
    inet:url#mal | al4.url.submit --force

Usage: al4.url.submit [options]

Options:

  --help                      : Display the command usage.
  --debug                     : Show verbose debug output.
  --yield                     : Yield the newly created nodes.
  --download                  : Download the file associated to the URL submission. This will not execute if the --nowait option is used.
  --force                     : Ignore Assemblyline results cache and force a re-scan.
  --nowait                    : Do not wait for analysis results.

Inputs:

    inet:url - Any inet:url node.
```
