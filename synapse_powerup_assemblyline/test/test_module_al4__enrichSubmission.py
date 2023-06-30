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
    async def test_enrichSubmission(self):
        """
        Validate the associated analytical result nodes are created and yielded.
        """
        async with self.getTestCoreWithPkg() as core:
            sid = "2T3kDaR5JukKbYPM0sBkjq"
            q = """ 
                // Setup the cache for the test
                $lib.jsonstor.cacheset(("power-ups","al4","cache","submission","tree"), $sid, $submission_tree_result)
                $lib.jsonstor.cacheset(("power-ups","al4","cache","submission","ontology"), $sid, $raw_ont_result)
            
                $mod = $lib.import(al4)
                
                for $n in $mod.enrichSubmission($sid) {
                    yield $n
                }
                """
            submission_tree_result = self.getTestFileJson(
                "submission-tree.multiple_results.json"
            )
            raw_result = self.getTestFileJsonAsRawOntologyResult(
                "ontology_results/raw_ontresults.submission.multiple_results.json"
            )
            opts = {
                "vars": {
                    "raw_ont_result": raw_result,
                    "submission_tree_result": submission_tree_result,
                    "sid": sid,
                }
            }
            nodes = await core.nodes(q, opts=opts)

            # debug
            # for nod in nodes:
            #    log.warning(nod.pack(dorepr=True))

            expected = [
                (
                    "file:bytes",
                    "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                ),
                (
                    "file:bytes",
                    "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb8c",
                ),
                ("inet:fqdn", "foo.local"),
                ("inet:url", "https://bar.local/"),
            ]

            self.len(len(expected), nodes)

            # verify each node's ndef is found in the expected list
            for nod in nodes:
                self.isin(nod.ndef, expected)

    async def test_enrichSubmission_no_results(self):
        """
        Validate the file:bytes nodes are created, but nothing else
        """
        async with self.getTestCoreWithPkg() as core:
            sid = "2T3kDaR5JukKbYPM0sBkjq"
            q = """ 
                // Setup the cache for the test
                $lib.jsonstor.cacheset(("power-ups","al4","cache","submission","tree"), $sid, $submission_tree_result)
                $lib.jsonstor.cacheset(("power-ups","al4","cache","submission","ontology"), $sid, $raw_ont_result)
            
                $mod = $lib.import(al4)
                
                for $n in $mod.enrichSubmission($sid) {
                    yield $n
                }
                """
            submission_tree_result = self.getTestFileJson(
                "submission-tree.no_results.json"
            )
            raw_result = self.getTestFileJsonAsRawOntologyResult(
                "ontology_results/raw_ontresults.submission.no_results.json"
            )
            opts = {
                "vars": {
                    "raw_ont_result": raw_result,
                    "submission_tree_result": submission_tree_result,
                    "sid": sid,
                }
            }
            nodes = await core.nodes(q, opts=opts)

            # debug
            # for nod in nodes:
            #    log.warning(nod.pack(dorepr=True))

            expected = [
                (
                    "file:bytes",
                    "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                ),
            ]

            self.len(len(expected), nodes)

            # verify each node's ndef is found in the expected list
            for nod in nodes:
                self.isin(nod.ndef, expected)

    async def test_enrichSubmission_warnForImproperInputs(self):
        """
        validate than when the submission id (sid) is not specified,
         a warning message is raised and no node is yielded
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4)
                
                for $n in $mod.enrichSubmission($lib.null) {
                    yield $n
                }
                """
            nodes = await core.nodes(q)
            self.len(0, nodes)

            msgs = await core.stormlist(q)
            self.stormIsInWarn(
                "usaa-assemblyline4 - enrichSubmission expected sid",
                msgs,
            )
            # log.warning(msgs)
