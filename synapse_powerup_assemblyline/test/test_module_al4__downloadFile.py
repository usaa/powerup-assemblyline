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

    async def test_downloadFile_fileInAxon(self):
        """
        input: file:bytes
        Validate the file:bytes node is returned when the file is already in the axon
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
                
                for $n in $mod.downloadFile($getNod($sha256)) {
                    yield $n
                }
                """
            sha256 = "f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b"
            opts = {"vars": {"sha256": sha256}}
            nodes = await core.nodes(q, opts=opts)

            # debug
            # for nod in nodes:
            #    log.warning(nod.pack(dorepr=True))

            self.len(1, nodes)

            #
            # Approach: doing basic node validation, as lower level unit tests validated
            #  full details, including node props, light edges, and tags
            #
            expected = [
                {
                    "form": "file:bytes",
                    "valu": f"sha256:{sha256}",
                    "md5": "912ec803b2ce49e4a541068d495ab570",
                },
            ]
            for nod in nodes:
                self.isin(
                    {
                        "form": nod.ndef[0],
                        "valu": nod.ndef[1],
                        "md5": nod.props.get("md5"),
                    },
                    expected,
                )

        """
        input: hash:sha256
        Validate the file:bytes node is returned when the file is already in the axon

        NOTE: The al4.file.download command uses the divert command, which handles returning
         the appropriate node to the caller. e.g. if hash:sha256 is the input node, the divert
         command will take care of returning that node; even though this function returns 
         the file:bytes node
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
                    hash:sha256=$inp
                    return($node)
                }

                $mod = $lib.import(al4)
                
                for $n in $mod.downloadFile($getNod($sha256)) {
                    yield $n
                }
                """
            sha256 = "f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b"
            opts = {"vars": {"sha256": sha256}}
            nodes = await core.nodes(q, opts=opts)

            # debug
            # for nod in nodes:
            #    log.warning(nod.pack(dorepr=True))

            self.len(1, nodes)

            #
            # Approach: doing basic node validation, as lower level unit tests validated
            #  full details, including node props, light edges, and tags
            #
            expected = [
                {
                    "form": "file:bytes",
                    "valu": f"sha256:{sha256}",
                    "md5": "912ec803b2ce49e4a541068d495ab570",
                },
            ]
            for nod in nodes:
                self.isin(
                    {
                        "form": nod.ndef[0],
                        "valu": nod.ndef[1],
                        "md5": nod.props.get("md5"),
                    },
                    expected,
                )

    async def test_downloadFile_warnForImproperInputs(self):
        """
        validate than when a node other than file:bytes or hash:sha256 is specified, a
        warning message is raised and no node is yielded
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                function getNod() {
                    [it:dev:str=1234]
                    return($node)
                }

                $mod = $lib.import(al4)
                
                for $n in $mod.downloadFile($getNod()) {
                    yield $n
                }
                """
            nodes = await core.nodes(q)
            self.len(0, nodes)

            msgs = await core.stormlist(q)
            self.stormIsInWarn(
                "usaa-assemblyline4 - downloadFile expected file:bytes or hash:sha256 node.",
                msgs,
            )
            # log.warning(msgs)

        """
        validate than when a file:bytes node without a :sha256 property is the input, 
        warning message is raised and no node is yielded
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                function getNod() {
                    [file:bytes=*]
                    return($node)
                }

                $mod = $lib.import(al4)
                
                for $n in $mod.downloadFile($getNod()) {
                    yield $n
                }
                """
            nodes = await core.nodes(q)
            self.len(0, nodes)

            msgs = await core.stormlist(q)
            self.stormIsInWarn(
                "usaa-assemblyline4 - sha256 not found on requested node.",
                msgs,
            )
