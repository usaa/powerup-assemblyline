import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ingest_Tests(t_utils.TestUtils):
    async def test_addAnalysisResults(self):
        """
        Happy path - validate nodes are created as expected.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ingest)

                for $n in $mod.addAnalysisResults($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.fileresult.foosvc.json"
                    )
                }
            }
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

            self.len(len(expected), nodes)

            # verify each node's ndef is found in the expected list
            for nod in nodes:
                self.isin(nod.ndef, expected)

        """
        Happy path - validate only the file:bytes node is created as there are no
         analytic results to extract
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ingest)

                for $n in $mod.addAnalysisResults($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.fileresult.no_artifacts.json"
                    )
                }
            }
            nodes = await core.nodes(q, opts=opts)

            expected = [
                (
                    "file:bytes",
                    "sha256:1a107c3ece1880cbbdc0a6c0817624b0dd033b02ebaf7fa366306aaca22c103d",
                )
            ]

            self.len(len(expected), nodes)

            # verify each node's ndef is found in the expected list
            for nod in nodes:
                self.isin(nod.ndef, expected)

    async def test_raises_NoSuchImpl(self):
        """
        Verify Raises NoSuchImpl due to an unsupported ontology odm version
        """
        async with self.getTestCoreWithPkg() as core:
            # missing sha256 prop in input dict
            q = """ 
                $mod = $lib.import(al4.ingest)
                return($mod.addAnalysisResults($ont_result_dict))
                """
            opts = {"vars": {"ont_result_dict": {"odm_version": "2.0"}}}

            with self.raises(s_exc.NoSuchImpl) as exc:
                await core.callStorm(q, opts=opts)
            self.isin(
                "NoSuchImpl Exception - Assemblyline Ontology version not supported. Version=",
                exc.exception.get("mesg"),
            )
