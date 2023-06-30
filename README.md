# usaa-assemblyline4 Power-Up

`usaa-assemblyline4` is a Synapse Rapid Power-Up that allows Synapse to interact with Assemblyline v4.

See the package docs in Optic for other general information and usage.

## Technical Approach

### Assemblyline API

The Assemblyline API can present results via multiple endpoints. The major endpoint choices are `/api/v4/submission`,
`/api/v4/ontology`, and `/api/v4/file` for retrieving analytical results for submissions and individual files. The
ontology API was chosen as its general purpose is to provide results to other systems whereas the other APIs are
intended to present results to a user and returns much more data.

### Model

The model is extended by adding the following properties:

| form         | property             | notes                                                                               |
| ------------ | -------------------- | ----------------------------------------------------------------------------------- |
| `file:bytes` | `_assemblyline:type` | File type as defined by Assemblyline. e.g. `executable/windows/pe32`, `code/python` |

### Modules

| module             | API | purpose                                                                                                                      |
| ------------------ | --- | ---------------------------------------------------------------------------------------------------------------------------- |
| `al4`              | yes | Interface into this Power-Up's functionality. Any functions here can be used by other modules or commands.                   |
| `al4.common`       | no  | Internal functions commonly used across other Assemblyline Power-Up modules.                                                 |
| `al4.ingest`       | no  | Internal functions used to ingest data into the Cortex.                                                                      |
| `al4.ontology`     | no  | Internal functions for obtaining the proper Assemblyline ontology parser.                                                    |
| `al4.ontology.v1x` | no  | Internal functions implementing the Assemblyline ontology parser for version 1.x ontologies.                                 |
| `al4.privsep`      | no  | Internal functions considered to be privileged.                                                                              |
| `al4.setup`        | no  | Internal functions which are meant to be used by the other module code that needs access to various Power-Up configurations. |
| `al4.setup.admin`  | no  | Internal functions which are meant to get and set global configurations for all users of this Power-Up.                      |
| `al4.setup.user`   | no  | Internal functions which are used to set user specific configurations of this Power-Up.                                      |

### Permissions

Permissions can be a bit tricky. This explains the approach used to secure the Power-Ups modules and Commands.

This assumes you understand the following:
<https://synapse.docs.vertex.link/en/latest/synapse/devguides/power-ups.html#privileged-modules>

#### Module Security

This section explains this Power-Up's approach for Storm module security.

Only the modules considered to be an API should be imported directly by Storm code and the only module considered to be
an API is `al4`. e.g. `$lib.import(al4)`.

Unless mentioned below, all modules can technically be imported by any user as nothing prevents a user from importing
other modules that don't have explicit permissions defined in the package definition. Whether the module functions will
depend on the user's underlying Cortex permissions. Nothing sensitive is kept in the other modules which is why there
are no explicit Power-Up permissions defined. However, if any of these modules imports another module that requires
explicit permissions, that gate check will be performed. i.e. Even though the package definition does not explicitly
require permissions to import `al4`, that module imports `al4.privsep` which does explicitely require the user to have
the permission `power-ups.al4.user`. Therefore the `al4` module indirectly requires the user to have that permission.

##### al4.privsep

This module contains code considered to be privileged.

Permissions are elevated to `asroot` and the user must be a member of the `power-ups.al4.user` group.

Among other things, this module contains functions to call the underlying Assemblyline API. This requires permissions to
make those calls and access the Power-Up's configurations such as global API keys or Power-Up proxy configurations.

##### al4.setup

This module contains `get` functions which are meant to be used by the other module code that needs access to various
Power-Up configurations. Storm commands that need to set these related variables should do so through the
`al4.setup.user` and `al4.setup.admin` modules.

Permissions are not elevated to `asroot`. So if a Synapse user that is not a cortex admin tries to import this module
directly, it will only return user related variables (`$lib.user.vars`) and nothing set globally (`$lib.globals`).
e.g. API keys for accessing Assemblyline or the proxy configuration.

This module is meant to be used by the `al4.privsep` module which does elevate permissions. When that code needs access
to an API key for Assemblyline, it calls this `al4.setup` module to retrieve it using it's elevated permissions. The
user must be a member of `power-ups.al4.user` to import the `al4.privsep` module.

##### al4.setup.admin

This modules contains `get` and `set` functions which are meant to get and set global configurations for all users of
this Power-Up.

Permissions are elevated to `asroot` and the user must be a member of the `power-ups.al4.admin` group.

##### al4.setup.user

This module contains `get` and `set` functions which are available to be set for user specific configurations of this
Power-Up. i.e. Any `al4.setup` command with a `--self` option.

Permissions are not elevated to `asroot`.

#### Command Security

Any setup command that sets configurations for all users requires the `power-ups.al4.admin` role defined to prevent
unauthorized users from executing the commands.

Any setup command that can also set user specific configurations (`--self` option) requires the user to be a member of
the `power-ups.al4.user` group. e.g. the `al4.setup.apicreds` command. The approach used for module security will
prevent users that are not a member of `power-ups.al4.admin` from setting global configurations.

## Deployment

### How to install

The installation of this Power-Up can be done via the `./installer/install-storm-service.py` python script.

### How to update

Update the `package.yml` version number and simply re-run the package installation python script.

### How to uninstall

Remove the package via Optic.

## Development

### Unit Tests

`pytest` is used to execute the unit tests. Unit tests cover the majority of the functionality.

They do NOT currently cover any functionality that requires access to the Assemblyline API. A future effort can create
a mock of that API to provide better unit test coverage.

## Troubleshooting

- Start by looking in the cortex logs as various messages are written to the cortex logs by this Power-Up.
