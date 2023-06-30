import logging

import pytest

import synapse.exc as s_exc

import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_privsep_Tests(t_utils.TestUtils):
    async def test__getAPICreds(self):
        """
        Validate creds returned when configured
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                
                $setupMod = $lib.import(al4.setup.user)
                $setupMod.setUserAPICreds(user, apikey)

                $mod = $lib.import(al4.privsep)

                return ($mod._getAPICreds())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq({"user": "user", "key": "apikey", "scope": "current-user"}, valu)

    async def test__getAPICreds_raisesExc(self):
        """
        Validate when the API creds are not specified, an exception is raised
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.privsep)

                return ($mod._getAPICreds())
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API creds are not configured. Run al4.setup.apicreds",
                exc.exception.get("mesg"),
            )
