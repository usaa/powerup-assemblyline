import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_Tests(t_utils.TestUtils):
    async def test_getProxy(self):
        """
        Validate API Host is returned
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $setupAdminMod = $lib.import(al4.setup.admin)
                $setupAdminMod.setGlobalProxy("http://yourproxy:8080")

                $mod = $lib.import(al4.setup)

                return($mod.getProxy())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq("http://yourproxy:8080", valu)

    async def test_getProxy_returns_null(self):
        """
        Verify returns $lib.null when the global proxy is not set
        """
        async with self.getTestCoreWithPkg() as core:
            # Test with global creds
            q = """ 
                $mod = $lib.import(al4.setup)
                return($mod.getProxy())
                """
            valu = await core.callStorm(q)
            self.none(valu)

    async def test_getProxy_raises_AuthDeny_noAsRootPerms(self):
        """
        Verify Raises AuthDeny for a user that does not have asRoot permissions
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user1")

            q = """ 
                $setupAdminMod = $lib.import(al4.setup.admin)
                $setupAdminMod.setGlobalProxy("http://yourproxy:8080")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user1") as asuser1:
                q = """
                $mod = $lib.import(al4.setup)
                return($mod.getProxy())
                """
                await self.asyncraises(s_exc.AuthDeny, asuser1.callStorm(q))
