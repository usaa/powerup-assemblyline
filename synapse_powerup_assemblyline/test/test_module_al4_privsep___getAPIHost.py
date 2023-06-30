import logging

import pytest

import synapse.exc as s_exc

import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_privsep_Tests(t_utils.TestUtils):
    async def test__getAPICreds(self):
        """
        Validate api host returned when configured
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $setupMod = $lib.import(al4.setup.admin)
                $setupMod.setGlobalAPIHost("al4.local")

                $mod = $lib.import(al4.privsep)

                return ($mod._getAPIHost())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq("al4.local", valu)

    async def test__getAPICreds_raisesExc(self):
        """
        Validate when the API host is not specified, an exception is raised
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.privsep)

                return ($mod._getAPIHost())
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API host is not configured. Run al4.setup.apihost",
                exc.exception.get("mesg"),
            )
