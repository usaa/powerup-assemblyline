import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.tests.utils as s_t_utils


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ontology_v1x_Tests(t_utils.TestUtils):
    async def test_addEmailAddrs_create(self):
        """
        Validate  an inet:email node is created.
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"

            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                // Add file:bytes to support the test
                $mod.addFile($ont_result_dict)
                
                for $n in $mod.addEmailAddrs($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.foosvc.json"
                    )
                }
            }
            nodes = await core.nodes(q, opts=opts)
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]
            file_node = (await core.nodes(f"file:bytes={sha256}"))[0]

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(2, nodes)

            #
            # validate the inet:email nodes

            expected = [
                {"form": "inet:email", "valu": "noreply@foo.local"},
                {"form": "inet:email", "valu": "noreply@bar.local"},
            ]
            expected_light_edges = [
                ("seen", ms_node.iden()),
                ("refs", file_node.iden()),
            ]

            for nod in nodes:
                self.isin({"form": nod.ndef[0], "valu": nod.ndef[1]}, expected)

                # Validate light edges to meta:source node
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test_addEmailAddrs_NoCreateSinceNoTag(self):
        """
        Validate an empty list is returned when there are no network.email.address tags
        in the ontology result.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addEmailAddrs($ont_result_dict) {
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

            self.len(0, nodes)

    async def test_addEmailAddrs_invalidValue(self):
        """
        Validate no nodes are created when only invalid values are present in the network.email.address tag.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addEmailAddrs($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.invalid_values.json"
                    )
                }
            }
            nodes = await core.nodes(q, opts=opts)

            self.len(0, nodes)
