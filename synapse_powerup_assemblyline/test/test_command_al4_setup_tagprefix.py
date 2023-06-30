import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Command_AL4_SETUP_TAGPREFIX_Tests(t_utils.TestUtils):
    async def test_run_command__setupTagPrefix(self):
        """
        - Show the default tag prefix
        - set the tag prefix
        - verify the tag prefix is set
        """
        async with self.getTestCoreWithPkg() as core:

            # now setup user with perms
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))
            await user.addRule((True, ("power-ups", "al4", "user")))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.tagprefix --show
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "The default tag prefix is in use: rep.assemblyline",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.tagprefix reptest.al4
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Setting Assemblyline Power-Up tag prefix for all users.",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)


                q = """
                al4.setup.tagprefix --show
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "A custom tag prefix is in use: reptest.al4",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)
