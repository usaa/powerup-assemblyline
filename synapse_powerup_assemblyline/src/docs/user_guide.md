# USAA-Assemblyline4 User Guide

USAA-Assemblyline4 adds new Storm commands that allow you to interact with Assemblyline v4.

## Getting Started

Check with your Admin to enable permissions for this power-up.

## Examples

### Setting your personal API key

To set-up a personal-use API key:

```text
> al4.setup.apicreds --self userid apikey
```

### Endpoints

Set the Assemblyline API host endpoint.

Note that only a user with `power-ups.al4.admin` can set the API endpoint.

```text
> al4.setup.apihost https://al.local:443
```

### Download a File from Assemblyline into Synapse

Download all files tagged with `#mal` into the axon.

```text
> file:bytes#mal | al4.file.download
```

Download a file from a `hash:sha256` node and yield the `file:bytes` node created

```text
> hash:sha256=5e52777a11d9b4728ae499a3437abaa8b3acefa1699f2928a4f02aa3e8f213e3 | al4.file.download --yield
```

### Enrich files in Synapse from Assemblyline file analysis results

Enrich the files tagged with `#mal` with all the latest analytic service results from Assemblyline 4.

```text
> file:bytes#mal | al4.file.enrich
```

### Enrich files in Synapse from an Assemblyline submission

Retrieve the Assemblyline analysis results for a given submission ignoring any local Synapse cache.

This will enrich Synapse with all files found in this submission.

```text
> al4.submission.enrich 44A8cH7F03NSF6qqOWOktq --asof now
```

### Submit files to Assemblyline for analysis

Submit files tagged with `#mal` to Assemblyline for analysis and wait for the results.

```text
> file:bytes#mal | al4.file.submit
```

Use the `--force` flag to ignore the Assemblyline analysis results cache and force a re-analysis of the file.

```text
> file:bytes#mal | al4.file.submit --force
```

### Submit a URL to Assemblyline for analysis

Submit `inet:url` nodes tagged with `#mal` to Assemblyline for analysis, but do not wait for the results.

```text
> inet:url#mal | al4.url.submit --nowait
```

Use the `--force` flag to ignore the Assemblyline analysis results cache and force a re-analysis of the file.

```text
> file:bytes#mal | al4.file.submit --force
```

# Use of meta:source nodes

USAA-Assemblyline4 uses a `meta:source` node and `-(seen)>` light weight edges to track nodes observed from the
Assemblyline API.

```text
> meta:source=be0d2eac8fdcbc2828a4e8fb375560a6
meta:source=be0d2eac8fdcbc2828a4e8fb375560a6
    .created = 2022/01/30 13:14:52.219
    :name = usaa-assemblyline4
    :type = usaa-assemblyline4
```

Storm can be used to filter nodes to include/exclude nodes which have been observed by USAA-Assemblyline4. The following
example shows how to filter the results of a query to include only results observed by USAA-Assemblyline4:

```text
> #maltag +{ <(seen)- meta:source=be0d2eac8fdcbc2828a4e8fb375560a6 }
```
