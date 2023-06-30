import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Command_AL4_SETUP_APIHOST_Tests(t_utils.TestUtils):
    async def test_run_command__setupAPIHost(self):
        """
        - Show the api host when not set
        - set the api host
        - Show the api host
        """
        async with self.getTestCoreWithPkg() as core:

            # now setup user with perms
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))
            await user.addRule((True, ("power-ups", "al4", "user")))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apihost --show
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Currently configured API host: None",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.apihost "https://al4.local"
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Setting the API host for all users.",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.apihost --show
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Currently configured API host: https://al4.local",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)
