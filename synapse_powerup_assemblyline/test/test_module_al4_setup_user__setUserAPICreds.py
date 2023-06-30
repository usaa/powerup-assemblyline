import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_user_Tests(t_utils.TestUtils):
    async def test_setUserAPICreds(self):
        """
        Validate API Creds are set
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

    async def test_setUserAPICreds_raises_BadArg(self):
        """
        Validate BadArg is raised when apiUser not specified
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup.user)
                $mod.setUserAPICreds($lib.null, "keyx")

                return($mod.getUserAPICreds())
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
                $mod = $lib.import(al4.setup.user)
                $mod.setUserAPICreds("userx", $lib.null)

                return($mod.getUserAPICreds())
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
                self.isin(
                    "BadArg Exception - missing param: apiKey",
                    exc.exception.get("mesg"),
                )

    async def test_setUserAPICreds_noPermsNeeded(self):
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
