import argparse
import aiohttp
import contextlib
import asyncio
import sys
import logging
import getpass
import yaml
import shutil

import synapse.tools.genpkg


log = logging.getLogger(__name__)


class SynapseRESTAPI:
    def __init__(self, http_api_host, http_api_port, userid, passwd):
        self.http_api_host = http_api_host
        self.http_api_port = http_api_port
        self.userid = userid
        self.passwd = passwd

    @contextlib.asynccontextmanager
    async def getHttpSess(self):

        jar = aiohttp.CookieJar(unsafe=True)
        conn = aiohttp.TCPConnector(ssl=False)

        async with aiohttp.ClientSession(cookie_jar=jar, connector=conn) as sess:
            if self.userid and self.passwd:
                if self.http_api_port is None:  # pragma: no cover
                    raise Exception("getHttpSess requires port for auth")

                async with sess.post(
                    f"https://{self.http_api_host}:{self.http_api_port}/api/v1/login",
                    json={"user": self.userid, "passwd": self.passwd},
                ) as resp:
                    retn = await resp.json()

            yield sess

    async def install_package(self, pkgdef):
        """
        Install the package
        :param pkgdef: pkgdef json created from genpkg Synapse tool
        :return: None
        """

        log.info("Installing storm service package.")
        async with self.getHttpSess() as sess:
            # Check deps first, then install package and configure it to deploy additional configs

            # Example $lib.pkg.deps() result
            # {'requires': [{'name': 'usaa-assemblyline4', 'version': '>0.1.0', 'optional': False, 'desc': None, 'ok': True, 'actual': '0.2.0'}], 'conflicts': []}

            body = {
                "query": """
                    // check deps first
                    
                    $depResults = $lib.pkg.deps($pkgdef)

                    $depMsgs = $lib.list()
                    for $dep in $depResults.requires {
                        if (not $dep.ok) {
                            $depMsgs.append($lib.str.format("{name} requires {version}. Current version is {actual}", name=$dep.name, version=$dep.version, actual=$dep.actual))
                        }
                    }
                    for $dep in $depResults.conflicts {
                        if (not $dep.ok) {
                            $depMsgs.append($lib.str.format("{name} {version} conflicts with current version {actual}", name=$dep.name, version=$dep.version, actual=$dep.actual))
                        }
                    }

                    if ($depMsgs.size() > 0) {
                        $lib.raise(BadConf, mesg=$lib.str.format("Failed Package dependencies: {msgs}", msgs=$depMsgs))
                    }
                    
                    $lib.pkg.add($pkgdef)
                """,
                "opts": {
                    "vars": {
                        "pkgdef": pkgdef,
                    },
                },
            }
            async with sess.get(
                f"https://{self.http_api_host}:{self.http_api_port}/api/v1/storm/call",
                json=body,
            ) as resp:
                resp.raise_for_status()
                r = await resp.json()
                if r.get("status") == "ok":
                    log.info("Package installed.")
                else:
                    raise Exception(f"Failed to install the package. Response={r}")


async def main(argv):
    logging.basicConfig(level="INFO")

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cortex-api-host",
        type=str,
        required=True,
        help="Cortex API host. e.g. localhost",
    )
    parser.add_argument(
        "--cortex-api-port", type=str, default=4443, help="Cortex API Port."
    )
    parser.add_argument(
        "--cortex-admin-user",
        type=str,
        required=True,
        help="Admin userid to install and configure package.",
    )
    parser.add_argument(
        "--cortex-admin-pwd",
        type=str,
        required=False,
        help="Admin password to install and configure package.",
    )

    parser.add_argument(
        "--package-def-path",
        type=str,
        required=True,
        help="File system path to the package definition's yml file.",
    )
    args = parser.parse_args()

    log.info("Starting storm service installation for usaa-assemblyline4.")

    # Copy the CHANGELOG.rst to the package docs
    shutil.copy(
        "../CHANGELOG.rst", "../synapse_powerup_assemblyline/src/docs/CHANGELOG_COPY.rst"
    )

    # Generate the package def through synapse genpkg tool
    log.info("Generating package definition from source.")
    pkgdef = synapse.tools.genpkg.loadPkgProto(path=args.package_def_path)

    # Initiate HTTP Session with the cortex for admin user
    if args.cortex_admin_pwd:
        cortex_admin_passwd = args.cortex_admin_pwd
    else:
        cortex_admin_passwd = getpass.getpass(
            prompt=f"Enter password for {args.cortex_admin_user}:"
        )

    synapi = SynapseRESTAPI(
        http_api_host=args.cortex_api_host,
        http_api_port=args.cortex_api_port,
        userid=args.cortex_admin_user,
        passwd=cortex_admin_passwd,
    )

    # Install the package to the cortex
    await synapi.install_package(pkgdef)

    log.info("Storm service installation and configuration completed.")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
