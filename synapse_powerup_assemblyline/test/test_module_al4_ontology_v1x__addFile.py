import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.tests.utils as s_t_utils


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ontology_v1x_Tests(t_utils.TestUtils):
    async def test_addFile_create(self):
        """
        Validate a file:bytes node is created.
            - all props set
            - all light edges set
            - tags set
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"

            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                yield $mod.addFile($ont_result_dict)
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.addFile.scenario1.json"
                    )
                }
            }
            nodes = await core.nodes(q, opts=opts)
            file_node = nodes[0]
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]
            webact_node = (await core.nodes('inet:web:acct=("al4.local", "admin")'))[0]
            webgrp_nodes = await core.nodes("inet:web:group")

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(1, nodes)

            #
            # validate the file:bytes as expected

            self.eq(file_node.props.get("sha256"), sha256)
            self.eq(file_node.props.get("md5"), "26ea3e520cb396587d32a7a01aa564bd")
            self.eq(
                file_node.props.get("sha1"), "bc2cb97f09f70bd21225232a41af6206a62fa182"
            )
            self.eq(
                file_node.props.get("_assemblyline:type"), "executable/windows/pe64"
            )
            self.eq(
                file_node.repr(name=".seen"),
                ("2023/03/24 15:35:33.326", "2023/03/24 15:35:33.327"),
            )

            expected_light_edges = [
                ("seen", ms_node.iden()),
                ("submitted", webact_node.iden()),
                ("refs", webgrp_nodes[0].iden()),
            ]

            # Validate light edges
            async for edge in file_node.iterEdgesN2():
                # log.warning(edge)
                self.isin(edge, expected_light_edges)

            self.len(0, await s_t_utils.alist(file_node.iterEdgesN1()))

            # Validate the tags
            expected_tags = [("rep.assemblyline.tlp.amber")]
            for tag in file_node.getTags(leaf=True):
                self.isin(tag[0], expected_tags)

            # Validate the light edges for inet:web:acct ledge
            expected_seen_light_edges = [
                ("seen", ms_node.iden()),
            ]
            async for edge in webact_node.iterEdgesN2():
                # log.warning(edge)
                self.isin(edge, expected_seen_light_edges)

            async for edge in webact_node.iterEdgesN1():
                self.eq(edge, ("submitted", file_node.iden()))

    async def test_addFile_missingDetails1(self):
        """
        Validate a file:bytes node is created.
            - all props set
                - .seen not specified
                - _assemblyline:type not specified
            - all light edges set
                - No (submitted) - no submitter
                - No (refs) - no tlp classification group
            - tags set
                - base tag only, has no TLP classification
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"

            q = """ 
                    $mod = $lib.import(al4.ontology.v1x)
                    
                    yield $mod.addFile($ont_result_dict)
                    """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.addFile.scenario2.json"
                    )
                }
            }
            nodes = await core.nodes(q, opts=opts)
            file_node = nodes[0]
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]
            webact_nodes = await core.nodes('inet:web:acct=("al4.local", "admin")')
            webgrp_nodes = await core.nodes("inet:web:group")

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(1, nodes)
            self.len(0, webact_nodes)
            self.len(0, webgrp_nodes)

            #
            # validate the file:bytes as expected

            self.eq(file_node.props.get("sha256"), sha256)
            self.eq(file_node.props.get("md5"), "26ea3e520cb396587d32a7a01aa564bd")
            self.eq(
                file_node.props.get("sha1"), "bc2cb97f09f70bd21225232a41af6206a62fa182"
            )
            self.eq(file_node.props.get("_assemblyline:type"), None)
            self.eq(file_node.repr(name=".seen"), None)

            expected_light_edges = [("seen", ms_node.iden())]

            # Validate light edges
            async for edge in file_node.iterEdgesN2():
                # log.warning(edge)
                self.isin(edge, expected_light_edges)

            self.len(0, await s_t_utils.alist(file_node.iterEdgesN1()))

            # Validate the tags
            expected_tags = [("rep.assemblyline")]
            for tag in file_node.getTags(leaf=True):
                self.isin(tag[0], expected_tags)
