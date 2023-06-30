import logging

import pytest

import synapse.exc as s_exc
import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_Tests(t_utils.TestUtils):
    async def test_getTagPrefix(self):
        """
        Validate the default Tag Prefix is returned when not overridden
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.setup)

                return($mod.getTagPrefix())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq("rep.assemblyline", valu)

        """
        Validate the overridden tag prefix is returned
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $setupAdminMod = $lib.import(al4.setup.admin)
                $setupAdminMod.setGlobalTagPrefix("rep.al")

                $mod = $lib.import(al4.setup)

                return($mod.getTagPrefix())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq("rep.al", valu)

    async def test_getTagPrefix_raises_AuthDeny_noAsRootPerms(self):
        """
        Verify Raises AuthDeny for a user that does not have asRoot permissions
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user1")

            q = """ 
                $setupAdminMod = $lib.import(al4.setup.admin)
                $setupAdminMod.setGlobalTagPrefix("rep.al")
                """
            await core.callStorm(q)

            async with core.getLocalProxy(user="user1") as asuser1:
                q = """
                $mod = $lib.import(al4.setup)
                return($mod.getTagPrefix())
                """
                await self.asyncraises(s_exc.AuthDeny, asuser1.callStorm(q))
