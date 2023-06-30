import logging

import pytest
import json

import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.tests.utils as s_t_utils


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_al4_Tests(t_utils.TestUtils):
    """
    NOTE: This has limited tests as the Assemblyline API is not being mocked

    TODO: Future, mock AL4 api so the full method can be tested
        e.g. cannot test getting the file children
    """

    async def test_submitFile_fileInAxon(self):
        """
        input: file:bytes
        Validate it gets to the point of trying to get the API creds and fails
        """
        async with self.getTestCoreWithPkg() as core:
            opts = {"vars": {"obj": b"asdf"}}
            await core.nodes("[ file:bytes=$obj ]", opts=opts)
            await core.axon.put(b"asdf")

            # debug
            # for nod in await core.nodes("file:bytes +$lib.bytes.has(:sha256)")
            #    log.warning(nod)

            q = """ 
                function getNod(inp) {
                    file:bytes=$inp
                    return($node)
                }

                $mod = $lib.import(al4)
                
                for $n in $mod.submitFile($getNod($sha256)) {
                    yield $n
                }
                """
            sha256 = "f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b"
            opts = {"vars": {"sha256": sha256}}

            with self.raises(s_exc.NeedConfValu) as exc:
                await core.callStorm(q, opts=opts)
            self.isin(
                "NeedConfValu Exception - The Assemblyline API host is not configured. Run al4.setup.apihost",
                exc.exception.get("mesg"),
            )

    async def test_submitFile_warnForImproperInputs(self):
        """
        validate than when a node other than file:bytes is specified,
         a warning message is raised and the input node is yielded
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                function getNod() {
                    [it:dev:str=1234]
                    return($node)
                }

                $mod = $lib.import(al4)
                
                for $n in $mod.submitFile($getNod()) {
                    yield $n
                }
                """
            nodes = await core.nodes(q)
            self.len(1, nodes)

            msgs = await core.stormlist(q)
            self.stormIsInWarn(
                "usaa-assemblyline4 - submitFile expected file:bytes node",
                msgs,
            )

            expected = [
                {
                    "form": "it:dev:str",
                    "valu": ("1234"),
                },
            ]
            for nod in nodes:
                self.isin({"form": nod.ndef[0], "valu": nod.ndef[1]}, expected)
