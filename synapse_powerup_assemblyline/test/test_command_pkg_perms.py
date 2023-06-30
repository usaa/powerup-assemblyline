import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Command_PKG_PERMS_Tests(t_utils.TestUtils):
    async def test_run_command__pkgPerms(self):
        """
        - validate output of pkg.perms.list command
        """
        async with self.getTestCoreWithPkg() as core:

            # now setup user with perms

            async with core.getLocalProxy() as core:
                q = """
                pkg.perms.list usaa-assemblyline4
                """
                msgs = await core.storm(q).list()

                expected_msgs = [
                    "Package (usaa-assemblyline4) defines the following permissions:",
                    "power-ups.al4.user               : Permissions needed to use the Assemblyline Power-up commands.",
                    "power-ups.al4.admin              : Permissions needed to manage configurations for the Assemblyline Power-up.",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)
