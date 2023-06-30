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
    async def test__addExecProc_create(self):
        """
        Validate a it:exec:proc node is created.
            - all props set
            - all light edges set
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"

            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                // add it:host to support the test
                $host = $mod._addHost($ont_result_dict)

                yield $mod._addExecProc($host, $ont_result_dict.file.sha256)
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
            host_node = (
                await core.nodes(f'it:host=$lib.guid("assemblyline4", {sha256})')
            )[0]

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(1, nodes)

            #
            # validate the file:bytes as expected

            self.eq(node.ndef[0], "it:exec:proc")
            self.eq(node.ndef[1], s_common.guid(("assemblyline4", sha256)))
            self.eq(node.props.get("host"), host_node.ndef[1])
            self.eq(node.props.get("sandbox:file"), f"sha256:{sha256}")

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
