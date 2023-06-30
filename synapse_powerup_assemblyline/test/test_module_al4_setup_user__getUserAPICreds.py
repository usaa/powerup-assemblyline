import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_user_Tests(t_utils.TestUtils):
    async def test_getUserAPICreds(self):
        """
        Validate API Creds are returned
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.user)
                $mod.setUserAPICreds("userx", "keyx")

                return($mod.getUserAPICreds())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq({"user": "userx", "key": "keyx", "scope": "current-user"}, valu)

    async def test_getUserAPICreds_returns_null(self):
        """
        Verify returns $lib.null when creds are not set
        """
        async with self.getTestCoreWithPkg() as core:
            # Test with global creds
            q = """ 
                $mod = $lib.import(al4.setup.user)
                return($mod.getUserAPICreds())
                """
            valu = await core.callStorm(q)
            self.none(valu)

    async def test_getUserAPICreds_noPermsNeeded(self):
        """
        Verify no perms are needed for a standard user to use this
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.user)
                $mod.setUserAPICreds("userx", "keyx")
                return($mod.getUserAPICreds())
                """
                valu = await asuser.callStorm(q)
                self.nn(valu)
                self.eq({"user": "userx", "key": "keyx", "scope": "current-user"}, valu)
