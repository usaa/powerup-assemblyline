import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_admin_Tests(t_utils.TestUtils):
    async def test_removeGlobalAPICreds(self):
        """
        Validate API Creds are removed
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalAPICreds("userx", "keyx")

                $creds = $mod.getGlobalAPICreds()

                if (not $creds) { $lib.raise(FatalErr, "")}
                
                $mod.removeGlobalAPICreds()

                return($mod.getGlobalAPICreds())
                """
            valu = await core.callStorm(q)
            self.none(valu)

        """
        Validate no error when creds are not there to remove
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.admin)
                
                $mod.removeGlobalAPICreds()

                return($mod.getGlobalAPICreds())
                """
            valu = await core.callStorm(q)
            self.none(valu)

    async def test_removeGlobalAPICreds_raises_AuthDeny_noAsRootPerms(self):
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
                return($mod.removeGlobalAPICreds())
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
                return($mod.removeGlobalAPICreds())
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_removeGlobalAPICreds_powerupUserInAdminGroup(self):
        """
        Verify returns as value when user is a member of power-ups.al4.admin group
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))

            async with self.getTestCoreWithPkg() as asuser:
                q = """ 
                    $mod = $lib.import(al4.setup.admin)
                    $mod.setGlobalAPICreds("userx", "keyx")

                    $creds = $mod.getGlobalAPICreds()

                    if (not $creds) { $lib.raise(FatalErr, "")}
                    
                    $mod.removeGlobalAPICreds()

                    return($mod.getGlobalAPICreds())
                    """
                valu = await asuser.callStorm(q)
                self.none(valu)
