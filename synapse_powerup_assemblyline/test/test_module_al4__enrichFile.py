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
    async def test_enrichFile(self):
        """
        input: file:bytes
        Validate the associated analytical result nodes are created and yielded.
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "76fcf3c26b464cfc30a40b78b7e6ac79034e31cf9fa377f81ee987a1a04e2b6a"
            q = """ 
                function getNod(inp) {
                    [file:bytes=$inp]
                    return($node)
                }
            
                // Setup the cache for the test
                $lib.jsonstor.cacheset(("power-ups","al4","cache","file","ontology"), $sha256, $raw_ont_result)
            
                $mod = $lib.import(al4)
                
                for $n in $mod.enrichFile($getNod($sha256)) {
                    yield $n
                }
                """
            raw_result = self.getTestFileJsonAsRawOntologyResult(
                "ontology_results/raw_ontresults.fileresult.multiple_results.json"
            )
            opts = {"vars": {"raw_ont_result": raw_result, "sha256": sha256}}
            nodes = await core.nodes(q, opts=opts)

            # debug
            # for nod in nodes:
            #    log.warning(nod.pack(dorepr=True))

            expected = [
                (
                    "file:bytes",
                    "sha256:76fcf3c26b464cfc30a40b78b7e6ac79034e31cf9fa377f81ee987a1a04e2b6a",
                ),
                ("inet:fqdn", "fonts.googleapis.com"),
                ("inet:fqdn", "www.w3.org"),
                ("inet:url", "https://fonts.googleapis.com"),
                ("inet:url", "https://fonts.gstatic.com"),
            ]

            self.len(len(expected), nodes)

            # verify each node's ndef is found in the expected list
            for nod in nodes:
                self.isin(nod.ndef, expected)

        """
        input: hash:sha256
        Validate the associated analytical result nodes are created and yielded.
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "76fcf3c26b464cfc30a40b78b7e6ac79034e31cf9fa377f81ee987a1a04e2b6a"
            q = """ 
                function getNod(inp) {
                    [hash:sha256=$inp]
                    return($node)
                }
            
                // Setup the cache for the test
                $lib.jsonstor.cacheset(("power-ups","al4","cache","file","ontology"), $sha256, $raw_ont_result)
            
                $mod = $lib.import(al4)
                
                for $n in $mod.enrichFile($getNod($sha256)) {
                    yield $n
                }
                """
            raw_result = self.getTestFileJsonAsRawOntologyResult(
                "ontology_results/raw_ontresults.fileresult.multiple_results.json"
            )
            opts = {"vars": {"raw_ont_result": raw_result, "sha256": sha256}}
            nodes = await core.nodes(q, opts=opts)

            # debug
            # for nod in nodes:
            #    log.warning(nod.pack(dorepr=True))

            expected = [
                (
                    "file:bytes",
                    "sha256:76fcf3c26b464cfc30a40b78b7e6ac79034e31cf9fa377f81ee987a1a04e2b6a",
                ),
                ("inet:fqdn", "fonts.googleapis.com"),
                ("inet:fqdn", "www.w3.org"),
                ("inet:url", "https://fonts.googleapis.com"),
                ("inet:url", "https://fonts.gstatic.com"),
            ]

            self.len(len(expected), nodes)

            # verify each node's ndef is found in the expected list
            for nod in nodes:
                self.isin(nod.ndef, expected)

    async def test_enrichFile_warnForImproperInputs(self):
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
                
                for $n in $mod.enrichFile($getNod()) {
                    yield $n
                }
                """
            nodes = await core.nodes(q)
            self.len(0, nodes)

            msgs = await core.stormlist(q)
            self.stormIsInWarn(
                "usaa-assemblyline4 - enrichFile expected file:bytes or hash:sha256 node.",
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
                
                for $n in $mod.enrichFile($getNod()) {
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
