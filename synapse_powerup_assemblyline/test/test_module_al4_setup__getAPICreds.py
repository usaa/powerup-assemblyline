import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_Tests(t_utils.TestUtils):
    async def test_getAPICreds(self):
        """
        Validate API Creds are returned
        """
        async with self.getTestCoreWithPkg() as core:
            # Test with global creds
            q = """ 
                $setupAdminMod = $lib.import(al4.setup.admin)
                $setupAdminMod.setGlobalAPICreds("userx", "keyx")

                $mod = $lib.import(al4.setup)

                return($mod.getAPICreds())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq({"user": "userx", "key": "keyx", "scope": "global"}, valu)

            # Now override with self creds and verify those are returned
            q = """ 
                $setupUserMod = $lib.import(al4.setup.user)
                $setupUserMod.setUserAPICreds("usery", "keyy")

                $mod = $lib.import(al4.setup)

                return($mod.getAPICreds())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq({"user": "usery", "key": "keyy", "scope": "current-user"}, valu)

    async def test_getAPICreds_returns_null(self):
        """
        Verify returns $lib.null when creds are not set
        """
        async with self.getTestCoreWithPkg() as core:
            # Test with global creds
            q = """ 
                $mod = $lib.import(al4.setup)
                return($mod.getAPICreds())
                """
            valu = await core.callStorm(q)
            self.none(valu)

    async def test_getAPICreds_raises_AuthDeny_noAsRootPerms(self):
        """
        Verify Raises AuthDeny for a user that does not have asRoot permissions
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user1")

            q = """ 
                $setupAdminMod = $lib.import(al4.setup.admin)
                $setupAdminMod.setGlobalAPICreds("userx", "keyx")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user1") as asuser1:
                q = """
                $mod = $lib.import(al4.setup)
                return($mod.getAPICreds())
                """
                await self.asyncraises(s_exc.AuthDeny, asuser1.callStorm(q))

        """
        Verify basic user with no asRoot permissions able to access when only 'self' creds in use
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user1")

            async with core.getLocalProxy(user="user1") as asuser1:
                q = """ 
                $setupUserMod = $lib.import(al4.setup.user)
                $setupUserMod.setUserAPICreds("usery", "keyy")

                $mod = $lib.import(al4.setup)

                return($mod.getAPICreds())
                """
                valu = await core.callStorm(q)
                self.nn(valu)
                self.eq({"user": "usery", "key": "keyy", "scope": "current-user"}, valu)
