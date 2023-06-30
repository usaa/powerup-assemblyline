import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.tests.utils as s_t_utils


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ontology_v1x_Tests(t_utils.TestUtils):
    async def test_addPasswords_create(self):
        """
        Validate a inet:passwd node is created.
            - all light edges set
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"

            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                // Add file:bytes to support the test
                $mod.addFile($ont_result_dict)

                for $n in $mod.addPasswords($ont_result_dict) {
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
            file_node = (await core.nodes(f"file:bytes={sha256}"))[0]
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(1, nodes)

            expected = [
                {"form": "inet:passwd", "valu": "infected"},
            ]
            expected_light_edges_n2 = [
                ("seen", ms_node.iden()),
            ]
            expected_light_edges_n1 = [
                ("refs", file_node.iden()),
            ]

            for nod in nodes:
                self.isin({"form": nod.ndef[0], "valu": nod.ndef[1]}, expected)

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges_n2)

                async for edge in nod.iterEdgesN1():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges_n1)

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test_addPasswords_NoCreateSinceNoTag(self):
        """
        Validate an empty list is returned when there are no info.password tags
        in the ontology result.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addPasswords($ont_result_dict) {
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
