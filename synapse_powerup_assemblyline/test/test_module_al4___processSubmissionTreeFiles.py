import logging

import pytest
import json

import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.tests.utils as s_t_utils


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_al4_Tests(t_utils.TestUtils):
    async def test__processSubmissionTreeFiles(self):
        """
        Validate
            - file:bytes nodes are recursively created for every node found in the sample submission tree
            - validate appropriate file:subfile relationships created
            - validate file:filepaths created as expected
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $mod = $lib.import(al4)

                for ($k, $v) in $submission_file_tree_api_result.api_response.tree {
                    for $n in $mod._processSubmissionTreeFiles($v) {
                        yield $n
                    }
                }
                """

            raw_result = self.getTestFileJson("submission-tree-test1.json")

            opts = {"vars": {"submission_file_tree_api_result": raw_result}}
            nodes = await core.nodes(q, opts=opts)

            expected = [
                (
                    "file:bytes",
                    "sha256:4788ad19357d68b49d0433c806d1b7fd9c990d536716522c122f8b0fdcaad664",
                ),
                (
                    "file:bytes",
                    "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                ),
                (
                    "file:bytes",
                    "sha256:7619d0f290811c0f147191b77e33d237a47ea312719d10f77ebd5efd2483677e",
                ),
                (
                    "file:bytes",
                    "sha256:b75f8852bd62c925fe0a257606d93b24049a71ee8bc1e9d5e08ea717b8125298",
                ),
                (
                    "file:bytes",
                    "sha256:d0cb028a6e95a6b7644ab24df0a2b66d6d40a0dc66cb241e308a44f6b9fe32ac",
                ),
                (
                    "file:bytes",
                    "sha256:d38a8b061a0c3bbd9c3bd66c664ff9fa10d3f74983c59134b2534f2a283998c2",
                ),
                (
                    "file:bytes",
                    "sha256:b8bda64293e33551cc8d77559abe23bbb24e84a29892866287c1c04b0301cd6e",
                ),
            ]

            self.len(len(expected), nodes)

            # verify each node's ndef is found in the expected list
            for nod in nodes:
                self.isin(nod.ndef, expected)

            #
            # validate subfile relationships are created
            #
            q = """
                file:subfile
            """
            subfile_nodes = await core.nodes(q, opts=opts)
            expected = [
                (
                    "file:subfile",
                    (
                        "sha256:4788ad19357d68b49d0433c806d1b7fd9c990d536716522c122f8b0fdcaad664",
                        "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                    ),
                ),
                (
                    "file:subfile",
                    (
                        "sha256:4788ad19357d68b49d0433c806d1b7fd9c990d536716522c122f8b0fdcaad664",
                        "sha256:b8bda64293e33551cc8d77559abe23bbb24e84a29892866287c1c04b0301cd6e",
                    ),
                ),
                (
                    "file:subfile",
                    (
                        "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                        "sha256:7619d0f290811c0f147191b77e33d237a47ea312719d10f77ebd5efd2483677e",
                    ),
                ),
                (
                    "file:subfile",
                    (
                        "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                        "sha256:b75f8852bd62c925fe0a257606d93b24049a71ee8bc1e9d5e08ea717b8125298",
                    ),
                ),
                (
                    "file:subfile",
                    (
                        "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                        "sha256:d0cb028a6e95a6b7644ab24df0a2b66d6d40a0dc66cb241e308a44f6b9fe32ac",
                    ),
                ),
                (
                    "file:subfile",
                    (
                        "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                        "sha256:d38a8b061a0c3bbd9c3bd66c664ff9fa10d3f74983c59134b2534f2a283998c2",
                    ),
                ),
            ]

            self.len(len(expected), subfile_nodes)

            # verify each node's ndef is found in the expected list
            for nod in subfile_nodes:
                self.isin(nod.ndef, expected)

            #
            # validate file:filepath nodes are created as expected
            #
            q = """
                file:filepath
            """
            fpath_nodes = await core.nodes(q, opts=opts)
            expected = [
                (
                    "file:filepath",
                    (
                        "sha256:4788ad19357d68b49d0433c806d1b7fd9c990d536716522c122f8b0fdcaad664",
                        "pskill64.exe.zip",
                    ),
                ),
                (
                    "file:filepath",
                    (
                        "sha256:75899c5ace600406503a937ef550ab0bbd0f6e0188b9e93e206beb1dfc79bb81",
                        "pskill64.exe",
                    ),
                ),
                (
                    "file:filepath",
                    (
                        "sha256:b8bda64293e33551cc8d77559abe23bbb24e84a29892866287c1c04b0301cd6e",
                        "__macosx/._pskill64.exe",
                    ),
                ),
                (
                    "file:filepath",
                    (
                        "sha256:7619d0f290811c0f147191b77e33d237a47ea312719d10f77ebd5efd2483677e",
                        "overlay",
                    ),
                ),
                (
                    "file:filepath",
                    (
                        "sha256:b75f8852bd62c925fe0a257606d93b24049a71ee8bc1e9d5e08ea717b8125298",
                        "certificate",
                    ),
                ),
                (
                    "file:filepath",
                    (
                        "sha256:b75f8852bd62c925fe0a257606d93b24049a71ee8bc1e9d5e08ea717b8125298",
                        "overlay",
                    ),
                ),
                (
                    "file:filepath",
                    (
                        "sha256:d0cb028a6e95a6b7644ab24df0a2b66d6d40a0dc66cb241e308a44f6b9fe32ac",
                        ".data",
                    ),
                ),
                (
                    "file:filepath",
                    (
                        "sha256:d38a8b061a0c3bbd9c3bd66c664ff9fa10d3f74983c59134b2534f2a283998c2",
                        "binary_0_2147483880_2147483894_1033",
                    ),
                ),
            ]

            self.len(len(expected), fpath_nodes)

            # verify each node's ndef is found in the expected list
            for nod in fpath_nodes:
                self.isin(nod.ndef, expected)
