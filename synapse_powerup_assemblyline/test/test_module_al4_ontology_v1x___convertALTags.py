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
    async def test__convertALTags_alTagOnly(self):
        """
        Validate the correct tag is returned when only the alTagName is specified
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                $alTagName = "technique.macro"
        
                return($mod._convertALTags($alTagName))
                """
            opts = {"vars": {"ont_result_dict": {}}}
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)

            expected_list = ["rep.assemblyline.technique.macro"]

            self.len(1, valu)

            for tag in valu:
                self.isin(tag, expected_list)

    async def test__convertALTags_alTagAndVals(self):
        """
        Validate the correct tag is returned when alTagName and alTagVals are specified
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                $alTagName = "attribution.actor"
                $alTagVals = $lib.list("FOO", "Bar")
        
                return($mod._convertALTags($alTagName, $alTagVals))
                """
            opts = {"vars": {"ont_result_dict": {}}}
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)

            expected_list = [
                "rep.assemblyline.attribution.actor.foo",
                "rep.assemblyline.attribution.actor.bar",
            ]

            self.len(len(expected_list), valu)

            for tag in valu:
                self.isin(tag, expected_list)

    async def test__convertALTags_NotProperSynapseTagVals(self):
        """
        Validate a normalized synapse tag is returned when an Assemblylien tag value does
         not conform to the synapse tag convention
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                $alTagName = "attribution.actor"
                $alTagVals = $lib.list(
                    "FOO BAR", 
                    "Foo-namE",
                    " Foo ",
                    "1!2@3#4$5%6^7&8*9(10)1-2_3=4+"
                )
        
                return($mod._convertALTags($alTagName, $alTagVals))
                """
            opts = {"vars": {"ont_result_dict": {}}}
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)

            expected_list = [
                "rep.assemblyline.attribution.actor.foo_bar",
                "rep.assemblyline.attribution.actor.foo_name",
                "rep.assemblyline.attribution.actor.foo",
                "rep.assemblyline.attribution.actor.1_2_3_4_5_6_7_8_9_10_1_2_3_4",
            ]

            self.len(len(expected_list), valu)

            for tag in valu:
                self.isin(tag, expected_list)

    async def test__convertALTags_NullVals(self):
        """
        Validate an empty list is returned if no alTagName specified
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                $alTagName = ""
                        
                return($mod._convertALTags($alTagName))
                """
            opts = {"vars": {"ont_result_dict": {}}}
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)

            self.len(0, valu)

            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                $alTagName = $lib.null
                        
                return($mod._convertALTags($alTagName))
                """
            opts = {"vars": {"ont_result_dict": {}}}
            valu = await core.callStorm(q, opts=opts)
            self.nn(valu)

            self.len(0, valu)
