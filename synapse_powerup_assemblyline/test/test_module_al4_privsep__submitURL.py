import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_privsep_Tests(t_utils.TestUtils):

    """
    NOTE: This has limited tests as the Assemblyline API is not being mocked

    TODO: Future, mock AL4 api so the full method can be tested
    """

    async def test_submitURL_Raises_BadArg(self):
        """
        Test that BadArg is raised when missing input param
        """
        async with self.getTestCoreWithPkg() as core:
            q = """
                $mod = $lib.import(al4.privsep)
                $inp = $lib.null
                return($mod.submitURL($inp, $lib.dict()))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - invalid arg urlNode - expected inet:url",
                exc.exception.get("mesg"),
            )

        """
        Test that BadArg is raised when incorrect node type
        """
        async with self.getTestCoreWithPkg() as core:
            q = """
                $mod = $lib.import(al4.privsep)
                [it:dev:str=test1]
                $inp = $node
                return($mod.submitURL($inp, $lib.dict()))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - invalid arg urlNode - expected inet:url",
                exc.exception.get("mesg"),
            )

    async def test_submitURL_Raises_NeedConfValu_for_no_api_host(self):
        """
        Verify Raises NeedConfValu when api host is not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.privsep)
                [inet:url="https://testme.local"]
                $inp = $node
                return($mod.submitURL($inp, $lib.dict()))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API host is not configured. Run al4.setup.apihost",
                exc.exception.get("mesg"),
            )

    async def test_submitURL_Raises_NeedConfValu_for_no_api_creds(self):
        """
        Verify Raises NeedConfValu when api creds are not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $setupMod = $lib.import(al4.setup.admin)
                $setupMod.setGlobalAPIHost("al4.local")

                $mod = $lib.import(al4.privsep)
                
                [inet:url="https://testme.local"]
                $inp = $node

                return($mod.submitURL($inp, $lib.dict()))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API creds are not configured. Run al4.setup.apicreds",
                exc.exception.get("mesg"),
            )
