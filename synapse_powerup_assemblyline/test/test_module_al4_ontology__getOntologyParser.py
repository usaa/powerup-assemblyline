import logging

import pytest

import synapse.exc as s_exc

import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_ontology_Tests(t_utils.TestUtils):
    async def test_getOntologyParser_v1x(self):
        """
        Validate that the v1x ontology module is returned
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology)

                // example ontology result dict 
                /*
                    {
                        "odm_type": "Assemblyline Result Ontology",
                        "odm_version": "1.3",
                        ...
                    }
                */
                $ontParserMod = $mod.getOntologyParser("1.3")
                
                return($ontParserMod.ontParserVer)
                """
            valu = await core.callStorm(q)
            self.nn(valu)
            self.eq("v1x", valu)

    async def test_raises_NoSuchImpl(self):
        """
        Validate that NoSuchImpl exception is raised
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology)
                $mod.getOntologyParser("2.0")
                return($lib.null)
                """
            with self.raises(s_exc.NoSuchImpl) as exc:
                await core.callStorm(q)
            self.isin(
                "NoSuchImpl Exception - Assemblyline Ontology version not supported. Version=",
                exc.exception.get("mesg"),
            )

            q = """ 
                $mod = $lib.import(al4.ontology)
                $mod.getOntologyParser("0.2")
                return($lib.null)
                """
            with self.raises(s_exc.NoSuchImpl) as exc:
                await core.callStorm(q)
            self.isin(
                "NoSuchImpl Exception - Assemblyline Ontology version not supported. Version=",
                exc.exception.get("mesg"),
            )

            q = """ 
                $mod = $lib.import(al4.ontology)
                $mod.getOntologyParser("")
                return($lib.null)
                """
            with self.raises(s_exc.NoSuchImpl) as exc:
                await core.callStorm(q)
            self.isin(
                "NoSuchImpl Exception - Assemblyline Ontology version not supported. Version=",
                exc.exception.get("mesg"),
            )

            q = """ 
                $mod = $lib.import(al4.ontology)
                $mod.getOntologyParser($lib.null)
                return($lib.null)
                """
            with self.raises(s_exc.NoSuchImpl) as exc:
                await core.callStorm(q)
            self.isin(
                "NoSuchImpl Exception - Assemblyline Ontology version not supported. Version=",
                exc.exception.get("mesg"),
            )
