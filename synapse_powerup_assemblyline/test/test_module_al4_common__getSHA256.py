import logging

import pytest

import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_common_Tests(t_utils.TestUtils):
    async def test_getSHA256(self):
        """
        test happy path to verify sha256 is returned from file:bytes or hash:sha256 input node
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.common)
                
                [file:bytes=sha256:09dbc68ddb28d620713e768ec85c6e8ad37112404047ccab51d602ee1580ed54]
                return($mod.getSHA256($node))
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq(
                "09dbc68ddb28d620713e768ec85c6e8ad37112404047ccab51d602ee1580ed54", valu
            )

            q = """ 
                $mod = $lib.import(al4.common)

                [hash:sha256=09dbc68ddb28d620713e768ec85c6e8ad37112404047ccab51d602ee1580ed54]
                return($mod.getSHA256($node))
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq(
                "09dbc68ddb28d620713e768ec85c6e8ad37112404047ccab51d602ee1580ed54", valu
            )

    async def test_getSHA256_returns_null(self):
        """
        Test that getSHA256() returns $lib.null when invalid node (invalid form) is input node
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.common)

                [it:dev:str='test']
                return($mod.getSHA256($node))
                """
            valu = await core.callStorm(q)
            self.none(valu)
