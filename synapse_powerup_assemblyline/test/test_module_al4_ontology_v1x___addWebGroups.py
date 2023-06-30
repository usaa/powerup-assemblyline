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
    async def test__addWebGroups_createSingleGrp(self):
        """
        Validate a single inet:web:group node is created.
            - all light edges set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                for $n in $mod._addWebGroups($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": {
                        "submission": {
                            "source_system": "al4.local",
                            "classification": "TLP:AMBER//SOCGRP",
                        }
                    }
                }
            }
            nodes = await core.nodes(q, opts=opts)
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(1, nodes)

            #
            # validate the inet:web:group as expected
            expected = [
                {
                    "form": "inet:web:group",
                    "valu": ("al4.local", "SOCGRP"),
                },
            ]
            expected_light_edges = [
                ("seen", ms_node.iden()),
            ]
            for nod in nodes:
                self.isin({"form": nod.ndef[0], "valu": nod.ndef[1]}, expected)

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test__addWebGroups_createMultipleTopLevelGrps(self):
        """
        Validate multiple inet:web:group nodes are created when multiple top level groups are selected.
            - all light edges set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                for $n in $mod._addWebGroups($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": {
                        "submission": {
                            "source_system": "al4.local",
                            "classification": "TLP:WHITE//REL TO ORGA, ORGB",
                        }
                    }
                }
            }
            nodes = await core.nodes(q, opts=opts)
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(2, nodes)

            #
            # validate the inet:web:group as expected
            expected = [
                {
                    "form": "inet:web:group",
                    "valu": ("al4.local", "ORGA"),
                },
                {
                    "form": "inet:web:group",
                    "valu": ("al4.local", "ORGB"),
                },
            ]
            expected_light_edges = [
                ("seen", ms_node.iden()),
            ]
            for nod in nodes:
                self.isin({"form": nod.ndef[0], "valu": nod.ndef[1]}, expected)

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test__addWebGroups_createMultipleSubGrps(self):
        """
        Validate multiple inet:web:group nodes are created when multiple sub groups are selected.
            - all light edges set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                for $n in $mod._addWebGroups($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": {
                        "submission": {
                            "source_system": "al4.local",
                            "classification": "TLP:AMBER//SOCGRP/HUNTGRP",
                        }
                    }
                }
            }
            nodes = await core.nodes(q, opts=opts)
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(2, nodes)

            #
            # validate the inet:web:group as expected
            expected = [
                {
                    "form": "inet:web:group",
                    "valu": ("al4.local", "SOCGRP"),
                },
                {
                    "form": "inet:web:group",
                    "valu": ("al4.local", "HUNTGRP"),
                },
            ]
            expected_light_edges = [
                ("seen", ms_node.iden()),
            ]
            for nod in nodes:
                self.isin({"form": nod.ndef[0], "valu": nod.ndef[1]}, expected)

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test__addWebGroups_NoGroupCreated(self):
        """
        Validate no inet:web:group node is created.
            - When no releaseability group is present, but a classification is still present
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                for $n in $mod._addWebGroups($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": {
                        "submission": {
                            "source_system": "al4.local",
                            "classification": "TLP:WHITE",
                        }
                    }
                }
            }
            nodes = await core.nodes(q, opts=opts)

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(0, nodes)

        """
        Validate no inet:web:group node is created.
            - When no classification object is present
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                for $n in $mod._addWebGroups($ont_result_dict) {
                    yield $n
                }
                """
            opts = {
                "vars": {
                    "ont_result_dict": {
                        "submission": {
                            "source_system": "al4.local",
                        }
                    }
                }
            }
            nodes = await core.nodes(q, opts=opts)

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(0, nodes)
