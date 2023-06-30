import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_admin_Tests(t_utils.TestUtils):
    async def test_setGlobalAPIHost(self):
        """
        Validate API Host is set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPIHost("https://al4.local")

                return($mod.getGlobalAPIHost())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq("https://al4.local", valu)

    async def test_setGlobalAPIHost_raises_BadArg(self):
        """
        Validate BadArg is raised when apiHost not specified
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPIHost($lib.null)

                return($mod.getGlobalAPIHost())
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
                self.isin(
                    "BadArg Exception - missing param: apiUser",
                    exc.exception.get("mesg"),
                )

    async def test_setGlobalAPIHost_raises_AuthDeny_noAsRootPerms(self):
        """
        Verify Raises AuthDeny for a user that is not a member of the power-ups.al4.admin group
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPIHost("https://al4.local")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                return($mod.setGlobalAPIHost())
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
                $mod.setGlobalAPIHost("https://al4.local")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                return($mod.setGlobalAPIHost())
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_setGlobalAPIHost_powerupUserInAdminGroup(self):
        """
        Verify returns as value when user is a member of power-ups.al4.admin group
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))

            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPIHost("https://al4.local")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPIHost("https://al4.local")

                return($mod.getGlobalAPIHost())
                """
                valu = await asuser.callStorm(q)
                self.nn(valu)
                self.eq("https://al4.local", valu)
