import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.common as s_common
import synapse.tests.utils as s_t_utils


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ontology_v1x_Tests(t_utils.TestUtils):
    async def test_addDynamicURIs_create(self):
        """
        Validate the appropriate nodes are created when a network.dynamic.uri tag is
        present in the ontology result.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addDynamicURIs($ont_result_dict) {
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

            # debug
            # for nod in nodes:
            # log.warn(nod.pack(dorepr=True))

            # Approach - validate the overall modeling structure of the related nodes.
            #  each of the lower level method unit tests will take care of the detailed
            #  node modeling validation

            self.len(2, nodes)

            #
            # validate the basic inet:dns:request nodes are returned
            sha256 = "75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"
            expected = [
                {
                    "form": "it:exec:url",
                    "valu": s_common.guid(
                        (
                            "assemblyline4",
                            sha256,
                            "http://go.microsoft.com/fwlink/?LinkID=123",
                        )
                    ),
                    "url": "http://go.microsoft.com/fwlink/?LinkID=123",
                    "sandbox:file": f"sha256:{sha256}",
                },
                {
                    "form": "it:exec:url",
                    "valu": s_common.guid(
                        ("assemblyline4", sha256, "https://testme.local/?f=123")
                    ),
                    "url": "https://testme.local/?f=123",
                    "sandbox:file": f"sha256:{sha256}",
                },
            ]
            expected_light_edges = [
                ("seen", ms_node.iden()),
            ]

            for nod in nodes:
                self.isin(
                    {
                        "form": nod.ndef[0],
                        "valu": nod.ndef[1],
                        "url": nod.props.get("url"),
                        "sandbox:file": nod.props.get("sandbox:file"),
                    },
                    expected,
                )

            #
            # Validate associated nodes are created and associated as expected

            # only expecting one it:host node
            host_nodes = await core.nodes(
                f'it:host=$lib.guid("assemblyline4", {sha256})'
            )
            self.len(1, host_nodes)

            # only expecting one it:exec:proc node
            proc_nodes = await core.nodes(
                f'it:exec:proc=$lib.guid("assemblyline4", {sha256})'
            )
            self.len(1, proc_nodes)
            self.eq(proc_nodes[0].props.get("host"), host_nodes[0].ndef[1])
            self.eq(proc_nodes[0].props.get("sandbox:file"), f"sha256:{sha256}")

            # validate the inet:fqdn nodes
            for item in expected:
                fqdn_nodes = await core.nodes(f'inet:url="{item.get("url")}"')
                self.len(1, fqdn_nodes)

            # validate the inet:dns:request nodes are associated properly to the host/proc
            for nod in nodes:
                self.eq(nod.props.get("host"), host_nodes[0].ndef[1])
                self.eq(nod.props.get("proc"), proc_nodes[0].ndef[1])

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test_addDynamicDomains_NoCreateSinceNoTag(self):
        """
        Validate an empty list is returned when there are no network.dynamic.uri tags
        in the ontology result.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addDynamicURIs($ont_result_dict) {
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

    async def test_addDynamicURIs_invalidValue(self):
        """
        Validate no nodes are created when only invalid values are present in the network.dynamic.uri tag.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addDynamicURIs($ont_result_dict) {
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
