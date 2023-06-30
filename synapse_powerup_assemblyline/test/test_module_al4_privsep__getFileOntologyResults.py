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

    async def test_getFileOntologyResults_Raises_BadArg(self):
        """
        Test that BadArg is raised when missing input param
        """
        async with self.getTestCoreWithPkg() as core:
            q = """
                $mod = $lib.import(al4.privsep)
                $inp = $lib.null
                return($mod.getFileOntologyResults($inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - missing param: sha256",
                exc.exception.get("mesg"),
            )

    async def test_getFileOntologyResults_Raises_NeedConfValu_for_no_api_host(self):
        """
        Verify Raises NeedConfValu when api host is not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.privsep)
                $inp = 'dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29ba7'
                return($mod.getFileOntologyResults($inp))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API host is not configured. Run al4.setup.apihost",
                exc.exception.get("mesg"),
            )

    async def test_getFileOntologyResults_Raises_NeedConfValu_for_no_api_creds(self):
        """
        Verify Raises NeedConfValu when api creds are not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $setupMod = $lib.import(al4.setup.admin)
                $setupMod.setGlobalAPIHost("al4.local")

                $mod = $lib.import(al4.privsep)
                
                $inp = 'dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29ba7'
                return($mod.getFileOntologyResults($inp))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API creds are not configured. Run al4.setup.apicreds",
                exc.exception.get("mesg"),
            )

    async def test_getFileOntologyResults_resultsInCache(self):
        """
        Validate raw results are returned when already in cache
        """
        async with self.getTestCoreWithPkg() as core:
            # for nod in await core.nodes("file:bytes +$lib.bytes.has(:sha256)")
            #    log.warning(nod)

            q = """ 
                $mod = $lib.import(al4.privsep)
                
                $sha256 = f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b
                $cachekey = $sha256
                $cachepath = ("power-ups",
                    "al4",
                    "cache",
                    "file",
                    "ontology")
                $lib.jsonstor.cacheset($cachepath, $cachekey, $api_result)

                return($mod.getFileOntologyResults($sha256))
                """

            opts = {
                "vars": {
                    "api_result": "ontresult1\nontresult2",
                }
            }
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)
            self.eq(valu, opts.get("vars").get("api_result"))
