import logging

import pytest

import synapse.exc as s_exc

import test.utils as t_utils
import synapse.tests.utils as s_test


log = logging.getLogger(__name__)


class Command_Security_AL4_FILE_DOWNLOAD_Tests(t_utils.TestUtils):
    async def test_run_command_with_no_perms_raises_AuthDeny(self):
        """
        Run the command and verify Raises AuthDeny for a user that does not have permissions.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.file.download
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_perms_succeeds(self):
        """
        Run the command and verify the --help message works for a user that has perms.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.file.download --help
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint("Download a file from Assemblyline", msgs)


class Command_Security_AL4_FILE_ENRICH_Tests(t_utils.TestUtils):
    async def test_run_command_with_no_perms_raises_AuthDeny(self):
        """
        Run the command and verify Raises AuthDeny for a user that does not have permissions.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.file.enrich
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_perms_succeeds(self):
        """
        Run the command and verify the --help message works for a user that has perms.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.file.enrich --help
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint(
                    "Enrich the specified file with all the latest analytic service results from Assemblyline 4",
                    msgs,
                )


class Command_Security_AL4_FILE_SUBMIT_Tests(t_utils.TestUtils):
    async def test_run_command_with_no_perms_raises_AuthDeny(self):
        """
        Run the command and verify Raises AuthDeny for a user that does not have permissions.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.file.submit
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_perms_succeeds(self):
        """
        Run the command and verify the --help message works for a user that has perms.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.file.submit --help
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint(
                    "Submit the specified file to Assemblyline for analysis and wait for the results",
                    msgs,
                )


class Command_Security_AL4_SETUP_APICREDS_Tests(t_utils.TestUtils):
    async def test_run_command_with_no_perms_raises_AuthDeny(self):
        """
        Run the command and verify Raises AuthDeny for a user that does not have permissions.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apicreds
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_no_admin_perms_raises_AuthDeny(self):
        """
        Run the command to set for global use and verify Raises AuthDeny for a user that
        does not have admin permissions.
        i.e. user must be a member of power-ups.al4.admin
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apicreds globaluser globalkey
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_perms_succeeds(self):
        """
        Run the command and verify the --help message works for a user that has perms.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apicreds --help
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint("Set the Assemblyline API user and key.", msgs)

        """
        Run the command with --self option to verify it works when user has perms
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apicreds --self user key
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint(
                    "Setting Assemblyline API creds for the current user", msgs
                )

                q = """
                al4.setup.apicreds --self --show-creds
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint("Currently configured API creds", msgs)

        """
        Run the command to set globally to verify it works when user has admin perms
        i.e. user must be a member of power-ups.al4.admin
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("power-ups", "al4", "admin")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apicreds globaluser globalkey
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint(
                    "Setting Assemblyline API creds for all users", msgs
                )

                q = """
                al4.setup.apicreds --show-creds
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint("Currently configured API creds", msgs)


class Command_Security_AL4_SETUP_APIHOST_Tests(t_utils.TestUtils):
    async def test_run_command_with_no_perms_raises_AuthDeny(self):
        """
        Run the command and verify Raises AuthDeny for a user that does not have permissions.
        i.e. user must be a member of power-ups.al4.admin
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apihost
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_perms_succeeds(self):
        """
        Run the command and verify the --help message works for a user that has perms.
        i.e. user must be a member of power-ups.al4.admin
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.apihost --help
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint("Set the Assemblyline API host endpoint.", msgs)


class Command_Security_AL4_SETUP_PROXY_Tests(t_utils.TestUtils):
    async def test_run_command_with_no_perms_raises_AuthDeny(self):
        """
        Run the command and verify Raises AuthDeny for a user that does not have permissions.
        i.e. user must be a member of power-ups.al4.admin
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.proxy
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_perms_succeeds(self):
        """
        Run the command and verify the --help message works for a user that has perms.
        i.e. user must be a member of power-ups.al4.admin
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.proxy --help
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint(
                    "Manage where the Assemblyline Power-Up proxies http traffic to.",
                    msgs,
                )


class Command_Security_AL4_SETUP_TAGPREFIX_Tests(t_utils.TestUtils):
    async def test_run_command_with_no_perms_raises_AuthDeny(self):
        """
        Run the command and verify Raises AuthDeny for a user that does not have permissions.
        i.e. user must be a member of power-ups.al4.admin
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.tagprefix
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_perms_succeeds(self):
        """
        Run the command and verify the --help message works for a user that has perms.
        i.e. user must be a member of power-ups.al4.admin
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.setup.tagprefix --help
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint(
                    "Set the tag prefix when recording Assemblyline tags.", msgs
                )


class Command_Security_AL4_SUBMISSION_ENRICH_Tests(t_utils.TestUtils):
    async def test_run_command_with_no_perms_raises_AuthDeny(self):
        """
        Run the command and verify Raises AuthDeny for a user that does not have permissions.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.submission.enrich 123
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_perms_succeeds(self):
        """
        Run the command and verify the --help message works for a user that has perms.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.submission.enrich --help
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint(
                    "Retrieve the analysis results for a given Assemblyline submission and enrich the corresponding nodes.",
                    msgs,
                )


class Command_Security_AL4_URL_SUBMIT_Tests(t_utils.TestUtils):
    async def test_run_command_with_no_perms_raises_AuthDeny(self):
        """
        Run the command and verify Raises AuthDeny for a user that does not have permissions.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.url.submit
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_run_command_with_perms_succeeds(self):
        """
        Run the command and verify the --help message works for a user that has perms.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                al4.url.submit --help
                """
                msgs = await asuser.storm(q).list()
                self.stormIsInPrint(
                    "Submit the specified URL to Assemblyline for analysis and wait for the results.",
                    msgs,
                )
