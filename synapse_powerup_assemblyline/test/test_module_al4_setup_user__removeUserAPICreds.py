import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_admin_Tests(t_utils.TestUtils):
    async def test_removeUserAPICreds(self):
        """
        Validate API Creds are removed
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.user)
                $mod.setUserAPICreds("userx", "keyx")

                $creds = $mod.getUserAPICreds()

                if (not $creds) { $lib.raise(FatalErr, "")}
                
                $mod.removeUserAPICreds()

                return($mod.getUserAPICreds())
                """
            valu = await core.callStorm(q)
            self.none(valu)

        """
        Validate no error when creds are not there to remove
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.user)
                
                $mod.removeUserAPICreds()

                return($mod.getUserAPICreds())
                """
            valu = await core.callStorm(q)
            self.none(valu)

    async def test_removeUserAPICreds_noPermsNeeded(self):
        """
        Verify no perms are needed for a standard user to use this
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.user)
                $mod.setUserAPICreds("userx", "keyx")
                
                $creds = $mod.getUserAPICreds()

                if (not $creds) { $lib.raise(FatalErr, "")}
                    
                $mod.removeUserAPICreds()

                return($mod.getUserAPICreds())
                """
                valu = await asuser.callStorm(q)
                self.none(valu)
