import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_Tests(t_utils.TestUtils):
    async def test_getAPIHost(self):
        """
        Validate API Host is returned
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $setupAdminMod = $lib.import(al4.setup.admin)
                $setupAdminMod.setGlobalAPIHost("https://al4.local")

                $mod = $lib.import(al4.setup)

                return($mod.getAPIHost())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq("https://al4.local", valu)

    async def test_getAPIHost_returns_null(self):
        """
        Verify returns $lib.null when the API host is not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup)
                return($mod.getAPIHost())
                """
            valu = await core.callStorm(q)
            self.none(valu)

    async def test_getAPIHost_raises_AuthDeny_noAsRootPerms(self):
        """
        Verify Raises AuthDeny for a user that does not have asRoot permissions
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user1")

            q = """ 
                $setupAdminMod = $lib.import(al4.setup.admin)
                $setupAdminMod.setGlobalAPIHost("https://al4.local")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user1") as asuser1:
                q = """
                $mod = $lib.import(al4.setup)
                return($mod.getAPIHost())
                """
                await self.asyncraises(s_exc.AuthDeny, asuser1.callStorm(q))
