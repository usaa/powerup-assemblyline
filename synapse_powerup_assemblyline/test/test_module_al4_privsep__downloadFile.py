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

    async def test_downloadFile_Raises_BadArg(self):
        """
        Test that BadArg is raised when missing input param
        """
        async with self.getTestCoreWithPkg() as core:
            q = """
                $mod = $lib.import(al4.privsep)
                $inp = $lib.null
                return($mod.downloadFile($inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - missing param: sha256",
                exc.exception.get("mesg"),
            )

    async def test_downloadFile_Raises_NeedConfValu_for_no_api_host(self):
        """
        Verify Raises NeedConfValu when api host is not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.privsep)
                $inp = 'dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29ba7'
                return($mod.downloadFile($inp))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API host is not configured. Run al4.setup.apihost",
                exc.exception.get("mesg"),
            )

    async def test_downloadFile_Raises_NeedConfValu_for_no_api_creds(self):
        """
        Verify Raises NeedConfValu when api creds are not set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $setupMod = $lib.import(al4.setup.admin)
                $setupMod.setGlobalAPIHost("al4.local")

                $mod = $lib.import(al4.privsep)
                
                $inp = 'dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29ba7'
                return($mod.downloadFile($inp))
                """
            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API creds are not configured. Run al4.setup.apicreds",
                exc.exception.get("mesg"),
            )

    async def test_downloadFile_fileInAxon(self):
        """
        Validate hashes are returned when the file is already in the axon
        """
        async with self.getTestCoreWithPkg() as core:
            opts = {"vars": {"obj": b"asdf"}}
            await core.nodes("[ file:bytes=$obj ]", opts=opts)
            await core.axon.put(b"asdf")

            # for nod in await core.nodes("file:bytes +$lib.bytes.has(:sha256)")
            #    log.warning(nod)
            # f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b

            q = """ 
                $mod = $lib.import(al4.privsep)
                
                $inp = 'f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b'
                return($mod.downloadFile($inp))
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq(
                {
                    "md5": "912ec803b2ce49e4a541068d495ab570",
                    "sha1": "3da541559918a808c2402bba5012f6c60b27661c",
                    "sha256": "f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b",
                    "sha512": "401b09eab3c013d4ca54922bb802bec8fd5318192b0a75f201d8b3727429080fb337591abd3e44453b954555b7a0812e1081c39b740293f765eae731f5a65ed1",
                },
                valu,
            )
