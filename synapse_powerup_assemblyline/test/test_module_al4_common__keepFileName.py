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
    async def test_keepFileName(self):
        """
        Validate various filenames are considered good or not to keep
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.common)
                
                $retn = $lib.dict(
                    "keep.1" = $mod.keepFileName("testme.exe"),
                    "keep.2" = $mod.keepFileName("t"),
                    "keep.3" = $mod.keepFileName("test_26ea3e520cb396587d32a7a01aa564bd"),
                    "no.1"   = $mod.keepFileName("75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81"),
                    "no.2"   = $mod.keepFileName("75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81.vir"),
                    "no.3"   = $mod.keepFileName("75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81.sample"),
                    "no.4"   = $mod.keepFileName("bc2cb97f09f70bd21225232a41af6206a62fa182"),
                    "no.5"   = $mod.keepFileName("bc2cb97f09f70bd21225232a41af6206a62fa182.mal"),
                    "no.6"   = $mod.keepFileName("26ea3e520cb396587d32a7a01aa564bd"),
                    "no.7"   = $mod.keepFileName("26ea3e520cb396587d32a7a01aa564bd.vir"),
                    "no.8"   = $mod.keepFileName("0"),
                    "no.9"   = $mod.keepFileName(".."),
                    "no.10"   = $mod.keepFileName("..."),
                    "no.11"   = $mod.keepFileName(""),
                    "no.12"  = $mod.keepFileName($lib.null)
                )
                return ($retn)
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq(
                {
                    "keep.1": True,
                    "keep.2": True,
                    "keep.3": True,
                    "no.1": False,
                    "no.2": False,
                    "no.3": False,
                    "no.4": False,
                    "no.5": False,
                    "no.6": False,
                    "no.7": False,
                    "no.8": False,
                    "no.9": False,
                    "no.10": False,
                    "no.11": False,
                    "no.12": False,
                },
                valu,
            )
