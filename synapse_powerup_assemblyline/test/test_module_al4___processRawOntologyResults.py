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
    async def test__processRawOntologyResults(self):
        """
        For this example with 2 ontology results, verify all nodes that should be created
         across both results are created.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4)

                for $n in $mod._processRawOntologyResults($raw_ont_result) {
                   yield $n
                }
                """

            raw_result = self.getTestFileJsonAsRawOntologyResult(
                "ontology_results/raw_ontresults.fileresult.multiple_results.json"
            )
            # debug
            # split = raw_result.split("\n")
            # for l in split:
            #    log.warning(l)

            opts = {"vars": {"raw_ont_result": raw_result}}
            nodes = await core.nodes(q, opts=opts)

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

            # It's +1 in this case b/c file:bytes is returned twice since the file:bytes will be created multiple times.
            # And there is no | uniq in the pipeline for this unit test.
            self.len(len(expected) + 1, nodes)

            # verify each node's ndef is found in the expected list
            for nod in nodes:
                self.isin(nod.ndef, expected)

    async def test__processRawOntologyResults_emptyResults(self):
        """
        For empty results, verify no nodes are created and no errors
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4)

                for $n in $mod._processRawOntologyResults($raw_ont_result) {
                   yield $n
                }
                """

            raw_result = ""

            opts = {"vars": {"raw_ont_result": raw_result}}
            nodes = await core.nodes(q, opts=opts)

            self.len(0, nodes)

        """
        For results with newlines and nothing else, verify no nodes are created and no errors
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4)

                for $n in $mod._processRawOntologyResults($raw_ont_result) {
                   yield $n
                }
                """

            raw_result = " \n   \n\n    \n   "

            opts = {"vars": {"raw_ont_result": raw_result}}
            nodes = await core.nodes(q, opts=opts)

            self.len(0, nodes)

    async def test__processRawOntologyResults_invalidJSON_raisesBadJsonText(self):
        """
        validate that if the results have invalid json that a BadJsonText exc raised
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4)

                for $n in $mod._processRawOntologyResults($raw_ont_result) {
                   yield $n
                }
                """

            raw_result = "invalidjson"

            opts = {"vars": {"raw_ont_result": raw_result}}
            with self.raises(s_exc.BadJsonText) as exc:

                nodes = await core.nodes(q, opts=opts)
                self.len(0, nodes)

    async def test__processRawOntologyResults_valid_and_invalid_json(self):
        """
        This test combines valid and invalid json results. Same test as the main test
         above plus and invalid json line.

         BadJsonText exc should be raised and processing stopped.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4)

                for $n in $mod._processRawOntologyResults($raw_ont_result) {
                   yield $n
                }
                """

            raw_result = self.getTestFileJsonAsRawOntologyResult(
                "ontology_results/raw_ontresults.fileresult.multiple_results.json"
            )
            raw_result = raw_result + "\ninvalidjson\n"

            opts = {"vars": {"raw_ont_result": raw_result}}
            with self.raises(s_exc.BadJsonText) as exc:

                nodes = await core.nodes(q, opts=opts)
                self.len(0, nodes)

