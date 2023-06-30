import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_admin_Tests(t_utils.TestUtils):
    async def test_setGlobalAPICreds(self):
        """
        Validate API Creds are set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPICreds("userx", "keyx")

                return($mod.getGlobalAPICreds())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq({"user": "userx", "key": "keyx", "scope": "global"}, valu)

    async def test_setGlobalAPICreds_raises_BadArg(self):
        """
        Validate BadArg is raised when apiUser not specified
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPICreds($lib.null, "keyx")

                return($mod.getGlobalAPICreds())
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
                self.isin(
                    "BadArg Exception - missing param: apiUser",
                    exc.exception.get("mesg"),
                )

        """
        Validate BadArg is raised when apiKey not specified
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPICreds("userx", $lib.null)

                return($mod.getGlobalAPICreds())
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
                self.isin(
                    "BadArg Exception - missing param: apiKey",
                    exc.exception.get("mesg"),
                )

    async def test_setGlobalAPICreds_raises_AuthDeny_noAsRootPerms(self):
        """
        Verify Raises AuthDeny for a user that is not a member of the power-ups.al4.admin group
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPICreds("userx", "keyx")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                return($mod.setGlobalAPICreds())
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

        """
        Verify AuthDeny for a user that is a member of the power-ups.al4.user group
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))

            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPICreds("userx", "keyx")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                return($mod.setGlobalAPICreds())
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_setGlobalAPICreds_powerupUserInAdminGroup(self):
        """
        Verify returns as value when user is a member of power-ups.al4.admin group
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))

            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPICreds("userx", "keyx")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPICreds("userx", "keyx")

                return($mod.getGlobalAPICreds())
                """
                valu = await asuser.callStorm(q)
                self.nn(valu)
                self.eq({"user": "userx", "key": "keyx", "scope": "global"}, valu)
