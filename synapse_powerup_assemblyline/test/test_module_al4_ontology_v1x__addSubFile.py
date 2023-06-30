import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.tests.utils as s_t_utils


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ontology_v1x_Tests(t_utils.TestUtils):
    async def test_addSubFile_create(self):
        """
        Validate a file:subfile node is created.
            - all light edges set
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "22a846c0054b26e996a9060ba85569f03a6a820ddc9a7066ecbccbc665e690bf"

            q = """ 
                $mod = $lib.import(al4.ontology.v1x)
                
                // Add file:bytes to support the test
                $mod.addFile($ont_result_dict)

                yield $mod.addSubFile($ont_result_dict)
                """
            opts = {
                "vars": {
                    "ont_result_dict": self.getTestFileJson(
                        "ontology_results/ontresult.submission.childfile.extract.json"
                    )
                }
            }
            nodes = await core.nodes(q, opts=opts)
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]
            file_node = (await core.nodes(f"file:bytes={sha256}"))[0]
            parent_sha256 = (
                "d81fff7122296dfd423c6000380e1910855096ec8c8a09d4c26a56549511a78c"
            )

            # debug
            # for nod in nodes:
            #    log.warn(nod.pack(dorepr=True))

            self.len(1, nodes)

            #
            # validate the file:subfile as expected
            expected = [
                {
                    "form": "file:subfile",
                    "valu": (f"sha256:{parent_sha256}", f"sha256:{sha256}"),
                },
            ]
            expected_light_edges = [("seen", ms_node.iden())]

            for nod in nodes:
                self.isin(
                    {
                        "form": nod.ndef[0],
                        "valu": nod.ndef[1],
                    },
                    expected,
                )

                # Validate light edges
                async for edge in nod.iterEdgesN2():
                    # log.warning(edge)
                    self.isin(edge, expected_light_edges)

                self.len(0, await s_t_utils.alist(nod.iterEdgesN1()))

                # Validate no tags present
                self.len(0, nod.getTags())

    async def test_addSubFile_NoCreateSinceNoParent(self):
        """
        Validate a null return occurs when no file.parent object exists in the ontology result
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4.ontology.v1x)

                for $n in $mod.addSubFile($ont_result_dict) {
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
