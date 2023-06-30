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
    async def test__buildTagsForFileBytes_baseTagOnly(self):
        """
        Validate only the base tag is created
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                return($mod._buildTagsForFileBytes($ont_result_dict))
                """
            opts = {"vars": {"ont_result_dict": {}}}
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)

            expected_list = ["rep.assemblyline"]

            self.len(1, valu)

            for tag in valu:
                self.isin(tag, expected_list)

    async def test__buildTagsForFileBytes_classificationTag(self):
        """
        Validate base tag + classification tag
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                return($mod._buildTagsForFileBytes($ont_result_dict))
                """
            opts = {
                "vars": {
                    "ont_result_dict": {"submission": {"classification": "TLP:WHITE"}}
                }
            }
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)

            expected_list = ["rep.assemblyline", "rep.assemblyline.tlp.white"]

            self.len(2, valu)

            for tag in valu:
                self.isin(tag, expected_list)

    async def test__buildTagsForFileBytes_analyticResults(self):
        """
        Validate base tag + classification tag
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                return($mod._buildTagsForFileBytes($ont_result_dict))
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.foosvc.json"
                    )
                }
            }
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)

            # log.warning(valu)

            expected_list = [
                "rep.assemblyline",
                "rep.assemblyline.tlp.amber",
                "rep.assemblyline.attribution.actor.actorx",
                "rep.assemblyline.attribution.actor.actory",
                "rep.assemblyline.attribution.campaign.campaigna",
                "rep.assemblyline.attribution.campaign.campaignb",
                "rep.assemblyline.attribution.exploit.exploita",
                "rep.assemblyline.attribution.exploit.exploitb",
                "rep.assemblyline.attribution.family.familya",
                "rep.assemblyline.attribution.family.familyb",
                "rep.assemblyline.attribution.implant.implanta",
                "rep.assemblyline.attribution.implant.implantb",
                "rep.assemblyline.attribution.network.networka",
                "rep.assemblyline.attribution.network.networkb",
                "rep.assemblyline.technique.comms_routine",
                "rep.assemblyline.technique.config",
                "rep.assemblyline.technique.crypto",
                "rep.assemblyline.technique.keylogger",
                "rep.assemblyline.technique.macro",
                "rep.assemblyline.technique.masking_algo",
                "rep.assemblyline.technique.obfuscation",
                "rep.assemblyline.technique.packer.upx",
                "rep.assemblyline.technique.persistence",
                "rep.assemblyline.technique.shellcode",
            ]

            self.len(len(expected_list), valu)

            for tag in valu:
                self.isin(tag, expected_list)
