import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Command_AL4_SETUP_APICREDS_Tests(t_utils.TestUtils):
    async def test_run_command__setupCredsForGlobalUse(self):
        """
        - show when nothing set
        - Set them at global level
        - Show the creds 
        - Remove the creds
        """
        async with self.getTestCoreWithPkg() as core:

            # now setup user with perms
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))
            await user.addRule((True, ("power-ups", "al4", "user")))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apicreds --show-creds
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Currently configured API creds: None",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.apicreds userx apikeyx
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Setting Assemblyline API creds for all users.",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)


                q = """
                al4.setup.apicreds --show-creds
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Currently configured API creds: {'user': 'userx', 'key': 'apikeyx', 'scope': 'global'}",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)


                q = """
                al4.setup.apicreds --remove
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Removing the Assemblyline API creds for all users",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)


                q = """
                al4.setup.apicreds --show-creds
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Currently configured API creds: None",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

    async def test_run_command__setupCredsForCurrentUser(self):
        """
        - show when nothing set
        - Set them at user level
        - Show the creds 
        - Remove the creds
        """
        async with self.getTestCoreWithPkg() as core:

            # now setup user with perms
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apicreds --show-creds --self
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Currently configured API creds: None",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                q = """
                al4.setup.apicreds --self userx apikeyx
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Setting Assemblyline API creds for the current user.",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

            
                q = """
                al4.setup.apicreds --show-creds --self
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Currently configured API creds: {'user': 'userx', 'key': 'apikeyx', 'scope': 'current-user'}",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)

                
                q = """
                al4.setup.apicreds --remove --self
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Removing the Assemblyline API creds for the current user",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)


                q = """
                al4.setup.apicreds --show-creds --self
                """
                msgs = await asuser.storm(q).list()

                expected_msgs = [
                    "Currently configured API creds: None",
                ]
                for msg in expected_msgs:
                    self.stormIsInPrint(msg, msgs)
