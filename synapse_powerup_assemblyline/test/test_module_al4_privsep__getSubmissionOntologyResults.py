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

    async def test_getSubmissionOntologyResults_Raises_BadArg(self):
        """
        Test that BadArg is raised when missing input param
        """
        async with self.getTestCoreWithPkg() as core:
            q = """
                $mod = $lib.import(al4.privsep)
                $inp = $lib.null
                return($mod.getSubmissionOntologyResults($inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - missing param: sid",
                exc.exception.get("mesg"),
            )

    async def test_getSubmissionOntologyResults_Raises_NeedConfValu_for_no_api_host(
        self,
    ):
        """
        Verify Raises NeedConfValu when api host is not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.privsep)
                $inp = '31AzwEFtMkWSNo2rcMXxyA'
                return($mod.getSubmissionOntologyResults($inp))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API host is not configured. Run al4.setup.apihost",
                exc.exception.get("mesg"),
            )

    async def test_getSubmissionOntologyResults_Raises_NeedConfValu_for_no_api_creds(
        self,
    ):
        """
        Verify Raises NeedConfValu when api creds are not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $setupMod = $lib.import(al4.setup.admin)
                $setupMod.setGlobalAPIHost("al4.local")

                $mod = $lib.import(al4.privsep)
                
                $inp = '31AzwEFtMkWSNo2rcMXxyA'
                return($mod.getSubmissionOntologyResults($inp))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API creds are not configured. Run al4.setup.apicreds",
                exc.exception.get("mesg"),
            )

    async def test_getSubmissionOntologyResults_resultsInCache(self):
        """
        Validate raw results are returned when already in cache
        """
        async with self.getTestCoreWithPkg() as core:
            # for nod in await core.nodes("file:bytes +$lib.bytes.has(:sha256)")
            #    log.warning(nod)

            q = """ 
                $mod = $lib.import(al4.privsep)
                
                $sid = 31AzwEFtMkWSNo2rcMXxyA
                $cachekey = $sid
                $cachepath = ("power-ups",
                    "al4",
                    "cache",
                    "submission",
                    "ontology")
                $lib.jsonstor.cacheset($cachepath, $cachekey, $api_result)

                return($mod.getSubmissionOntologyResults($sid))
                """

            opts = {
                "vars": {
                    "api_result": "ontresult1\nontresult2\nontresult3",
                }
            }
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)
            self.eq(valu, opts.get("vars").get("api_result"))
