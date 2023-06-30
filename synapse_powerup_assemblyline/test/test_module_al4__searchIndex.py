import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_al4_Tests(t_utils.TestUtils):

    """
    NOTE: This has limited tests as the Assemblyline API is not being mocked

    TODO: Future, mock AL4 api so the full method can be tested
    """

    async def test_searchIndex_Raises_BadArg(self):
        """
        Test that BadArg is raised when missing input param
        """
        async with self.getTestCoreWithPkg() as core:
            q = """
                $mod = $lib.import(al4)
                $inp = $lib.null
                return($mod.searchIndex($inp, $inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - missing param: searchQuery",
                exc.exception.get("mesg"),
            )

            q = """
                $mod = $lib.import(al4)
                $inp = $lib.null
                return($mod.searchIndex("search", $inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - missing param: index",
                exc.exception.get("mesg"),
            )

            q = """
                $mod = $lib.import(al4)
                $inp = (['field1', 'field2'])
                return($mod.searchIndex("search", "submission", fields=$inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - fields param expects str",
                exc.exception.get("mesg"),
            )

            q = """
                $mod = $lib.import(al4)
                $inp = ({'key':'val'})
                return($mod.searchIndex("search", "submission", fields=$inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - fields param expects str",
                exc.exception.get("mesg"),
            )

    async def test_searchIndex_Raises_NeedConfValu_for_no_api_host(self):
        """
        Verify Raises NeedConfValu when api host is not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4)
                $inp = 'search'
                return($mod.searchIndex($inp, $inp))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API host is not configured. Run al4.setup.apihost",
                exc.exception.get("mesg"),
            )

    async def test_searchIndex_Raises_NeedConfValu_for_no_api_creds(self):
        """
        Verify Raises NeedConfValu when api creds are not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $setupMod = $lib.import(al4.setup.admin)
                $setupMod.setGlobalAPIHost("al4.local")

                $mod = $lib.import(al4)
                
                $inp = 'search'
                return($mod.searchIndex($inp, $inp))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API creds are not configured. Run al4.setup.apicreds",
                exc.exception.get("mesg"),
            )
