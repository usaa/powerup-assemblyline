import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class ModulModule_setup_admin_Testse_setup_Tests(t_utils.TestUtils):
    async def test_deleteGlobalProxy(self):
        """
        Validate Proxy is removed
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalProxy("http://yourproxy:8080")

                $val = $mod.getGlobalProxy()

                if (not $val) { $lib.raise(FatalErr, "")}
                
                $mod.deleteGlobalProxy()

                return($mod.getGlobalProxy())
                """
            valu = await core.callStorm(q)
            self.none(valu)

        """
        Validate no error when creds are not there to remove
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.admin)
                
                $mod.deleteGlobalProxy()

                return($mod.getGlobalProxy())
                """
            valu = await core.callStorm(q)
            self.none(valu)

    async def test_deleteGlobalProxy_raises_AuthDeny_noAsRootPerms(self):
        """
        Verify Raises AuthDeny for a user that is not a member of the power-ups.al4.admin group
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            q = """ 
                $mod = $lib.import(al4.setup.admin)
                $mod.setGlobalProxy("http://yourproxy:8080")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                return($mod.deleteGlobalProxy())
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
                $mod.setGlobalProxy("http://yourproxy:8080")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                return($mod.deleteGlobalProxy())
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_deleteGlobalProxy_powerupUserInAdminGroup(self):
        """
        Verify returns as value when user is a member of power-ups.al4.admin group
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))

            async with self.getTestCoreWithPkg() as asuser:
                q = """ 
                    $mod = $lib.import(al4.setup.admin)
                    $mod.setGlobalProxy("http://yourproxy:8080")

                    $val = $mod.getGlobalProxy()

                    if (not $val) { $lib.raise(FatalErr, "")}
                    
                    $mod.deleteGlobalProxy()

                    return($mod.getGlobalProxy())
                    """
                valu = await asuser.callStorm(q)
                self.none(valu)
