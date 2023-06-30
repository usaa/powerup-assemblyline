import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Command_AL4_SETUP_PROXY_Tests(t_utils.TestUtils):
    async def test_run_command__setupProxy(self):
        """
        - Show the default proxy
        - set the proxy
        - verify the proxy is set
        - remove the proxy
        - verify it is defaulted again
        - disable the use of the proxy
        - verify it is disabled
        """
        async with self.getTestCoreWithPkg() as core:

            # now setup user with perms
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))
            await user.addRule((True, ("power-ups", "al4", "user")))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.proxy --show-proxy
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Assemblyline Power-Up Proxy: <Using Cortex configured proxy>",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.proxy http://proxy.local:1080
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Setting proxy for the Assemblyline Power-Up for all users.",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.proxy --show-proxy
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Assemblyline Power-Up Proxy: http://proxy.local:1080",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.proxy --remove
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Removing the Assemblyline Power-Up configured proxy.",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.proxy --show-proxy
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Assemblyline Power-Up Proxy: <Using Cortex configured proxy>",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.proxy --disable
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Disabling proxy for the Assemblyline Power-Up.",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.proxy --show-proxy
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Assemblyline Power-Up Proxy: <Configured to not use a proxy>",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)
