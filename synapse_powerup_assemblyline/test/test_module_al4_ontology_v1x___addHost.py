import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.tests.utils as s_t_utils
import synapse.common as s_common

import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ontology_v1x_Tests(t_utils.TestUtils):
    async def test__addHost_create(self):
        """
        Validate a it:host node is created.
            - all props set
            - all light edges set
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"

            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                yield $mod._addHost($ont_result_dict)
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.foosvc.json"
                    )
                }
            }
            nodes = await core.nodes(q, opts=opts)
            node = nodes[0]
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(1, nodes)

            #
            # validate the file:bytes as expected

            self.eq(node.ndef[0], "it:host")
            self.eq(node.ndef[1], s_common.guid(("assemblyline4", sha256)))
            self.eq(node.props.get("desc"), "Assemblyline 4 Results")

            expected_light_edges = [
                ("seen", ms_node.iden()),
            ]

            # Validate light edges
            async for edge in node.iterEdgesN2():
                # log.warning(edge)
                self.isin(edge, expected_light_edges)

            self.len(0, await s_t_utils.alist(node.iterEdgesN1()))

            # Validate no tags present
            self.len(0, node.getTags())
