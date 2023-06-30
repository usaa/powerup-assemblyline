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
    async def test_addDynamicIPs_createIPv4(self):
        """
        Validate the appropriate nodes are created when a network.dynamic.ip tag is
        present in the ontology result for ipv4 hits.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addDynamicIPs($ont_result_dict) {
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
                    "form": "inet:flow",
                    "valu": s_common.guid(("assemblyline4", sha256, "13.107.4.52")),
                    "dst:ipv4": "13.107.4.52",
                    "sandbox:file": f"sha256:{sha256}",
                },
                {
                    "form": "inet:flow",
                    "valu": s_common.guid(("assemblyline4", sha256, "8.8.8.8")),
                    "dst:ipv4": "8.8.8.8",
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
                        "dst:ipv4": nod.reprs().get("dst:ipv4"),
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

            # validate the inet:ipv4 nodes
            for item in expected:
                ip_nodes = await core.nodes(f'inet:ipv4={item.get("dst:ipv4")}')
                self.len(1, ip_nodes)

            # validate the inet:flow nodes are associated properly to the host/proc
            for nod in nodes:
                self.eq(nod.props.get("src:host"), host_nodes[0].ndef[1])
                self.eq(nod.props.get("src:proc"), proc_nodes[0].ndef[1])

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test_addDynamicIPs_createIPv6(self):
        """
        Validate the appropriate nodes are created when a network.dynamic.ip tag is
        present in the ontology result for ipv6 hits.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addDynamicIPs($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.foosvc.ipv6.json"
                    )
                }
            }
            nodes = await core.nodes(q, opts=opts)
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            # Approach - validate the overall modeling structure of the related nodes.
            #  each of the lower level method unit tests will take care of the detailed
            #  node modeling validation

            self.len(1, nodes)

            #
            # validate the basic inet:dns:request nodes are returned
            sha256 = "75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"
            expected = [
                {
                    "form": "inet:flow",
                    "valu": s_common.guid(
                        (
                            "assemblyline4",
                            sha256,
                            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                        )
                    ),
                    "dst:ipv6": "2001:db8:85a3::8a2e:370:7334",
                    "sandbox:file": f"sha256:{sha256}",
                }
            ]
            expected_light_edges = [
                ("seen", ms_node.iden()),
            ]

            for nod in nodes:
                self.isin(
                    {
                        "form": nod.ndef[0],
                        "valu": nod.ndef[1],
                        "dst:ipv6": nod.props.get("dst:ipv6"),
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

            # validate the inet:ipv4 nodes
            for item in expected:
                ip_nodes = await core.nodes(f'inet:ipv6={item.get("dst:ipv6")}')
                self.len(1, ip_nodes)

            # validate the inet:flow nodes are associated properly to the host/proc
            for nod in nodes:
                self.eq(nod.props.get("src:host"), host_nodes[0].ndef[1])
                self.eq(nod.props.get("src:proc"), proc_nodes[0].ndef[1])

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test_addDynamicIPs_NoCreateSinceNoTag(self):
        """
        Validate an empty list is returned when there are no network.dynamic.ip tags
        in the ontology result.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addDynamicIPs($ont_result_dict) {
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
        Validate no nodes are created when only invalid values are present in the network.dynamic.ip tag.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addDynamicIPs($ont_result_dict) {
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
