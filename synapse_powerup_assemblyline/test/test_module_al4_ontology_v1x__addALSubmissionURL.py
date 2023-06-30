import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ontology_v1x_Tests(t_utils.TestUtils):
    async def test_addALSubmissionURL_create(self):
        """
        Validate  an inet:urlfile node is created linking the AL submission
        to the root file of the submission.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $commMod = $lib.import(al4.common)
                $mod = $lib.import(al4.ontology.v1x)

                $n = $mod.addALSubmissionURL($ont_result_dict)
                
                return(
                    $lib.dict(
                        'pnode'=$n.pack(dorepr=$lib.true),
                        'edges'=$n.edges(reverse=$lib.true), 
                        'metasrc_pnode'=$commMod.getMetaSource().pack(dorepr=$lib.true),
                    )
                )
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.foosvc.json"
                    )
                }
            }
            valu = await core.callStorm(q, opts=opts)

            pnode = valu.get("pnode")
            edges = valu.get("edges")

            # Main node validation
            self.nn(pnode)
            self.eq(
                (
                    "inet:urlfile",
                    (
                        "https://al4.local/submission/2T3kDaR5JukKbYPM0sBkjq",
                        "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                    ),
                ),
                s_node.ndef(pnode),
            )

            # only light edge to meta:source should be found
            await self.agenlen(1, edges)
            ledge_node_idens = s_node.iden(valu.get("metasrc_pnode"))
            async for e in edges:
                self.eq(e[0], "seen")
                self.isin(e[1], ledge_node_idens)

            # Validate no tags present
            self.len(0, s_node.tags(pnode))

    async def test_addALSubmissionURL_NoCreateSinceChildFile(self):
        """
        Validate an inet:urlfile node is NOT created as this is not a root file of the
        submission.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                return($mod.addALSubmissionURL($ont_result_dict))
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.childfile.extract.json"
                    )
                }
            }
            valu = await core.callStorm(q, opts=opts)

            self.none(valu)

    async def test_addALSubmissionURL_NoCreateSinceNoSubmissionData(self):
        """
        Validate an inet:urlfile node is NOT created as there is no submission related metadata.
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                return($mod.addALSubmissionURL($ont_result_dict))
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.fileresult.foosvc.json"
                    )
                }
            }
            valu = await core.callStorm(q, opts=opts)

            self.none(valu)
