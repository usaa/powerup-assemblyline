import logging

import pytest

import synapse.common as s_common
import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.tests.utils as s_t_utils


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ontology_v1x_Tests(t_utils.TestUtils):
    async def test_addYaraHits_create(self):
        """
        Validate the appropriate nodes are created when a file.rule.yara tag is
        present in the ontology result.
            - it:app:yara:match nodes with associated it:app:yara:rule
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addYaraHits($ont_result_dict) {
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

            self.len(2, nodes)

            #
            # validate the basic inet:dns:request nodes are returned
            sha256 = "75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"
            expected = [
                {
                    "form": "it:app:yara:match",
                    "valu": (
                        s_common.guid(("al4", "src1.Archive_in_LNK")),
                        f"sha256:{sha256}",
                    ),
                },
                {
                    "form": "it:app:yara:match",
                    "valu": (
                        s_common.guid(("al4", "src2.Long_RelativePath")),
                        f"sha256:{sha256}",
                    ),
                },
            ]
            expected_light_edges = [
                ("seen", ms_node.iden()),
            ]
            for nod in nodes:
                self.isin(
                    {"form": nod.ndef[0], "valu": nod.ndef[1]},
                    expected,
                )

                # validate .seen prop
                self.eq(
                    ("2023/03/30 20:54:49.817", "2023/03/30 20:54:49.818"),
                    nod.repr(name=".seen"),
                )

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

            # Validate the associated it:app:yara:rule nodes
            #
            expected_yara_rule_nodes = [
                {
                    "form": "it:app:yara:rule",
                    "valu": s_common.guid(("al4", "src1.Archive_in_LNK")),
                    "name": "src1.Archive_in_LNK",
                },
                {
                    "form": "it:app:yara:rule",
                    "valu": s_common.guid(("al4", "src2.Long_RelativePath")),
                    "name": "src2.Long_RelativePath",
                },
            ]
            yrule_nodes = await core.nodes(f"it:app:yara:rule", opts=opts)

            self.len(2, yrule_nodes)

            for nod in yrule_nodes:
                self.isin(
                    {
                        "form": nod.ndef[0],
                        "valu": nod.ndef[1],
                        "name": nod.props.get("name"),
                    },
                    expected_yara_rule_nodes,
                )

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test_addYaraHits_NoCreateSinceNoTag(self):
        """
        Validate an empty list is returned when there are no file.yara.rule tags
        in the ontology result.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addYaraHits($ont_result_dict) {
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
