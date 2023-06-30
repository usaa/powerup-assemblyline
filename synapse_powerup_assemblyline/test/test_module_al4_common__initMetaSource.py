import logging

import pytest

import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_common_Tests(t_utils.TestUtils):
    async def test_getMetaSource(self):
        """
        test happy path to verify meta:source is created upon importing al4.common
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.common)
                return($mod.getMetaSource().ndef())
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq(("meta:source", "be0d2eac8fdcbc2828a4e8fb375560a6"), valu)

            valu = await core.nodes("meta:source=be0d2eac8fdcbc2828a4e8fb375560a6")
            log.warning(valu)
            self.len(1, valu)
            self.eq("usaa-assemblyline4", valu[0].props.get("name"))
            self.eq("usaa-assemblyline4", valu[0].props.get("type"))
