import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node
import synapse.tests.utils as s_t_utils


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ingest_Tests(t_utils.TestUtils):
    async def test_addFile(self):
        """
        Validate returns file:bytes node with all props set; light edge set; and no file:filepaths created
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $commMod = $lib.import(al4.common)
                $mod = $lib.import(al4.ingest)

                $hashes = $lib.dict(
                    "sha256"=dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29baa,
                    "md5"=e108f38ff8e45bcc0bd02c084990b6ba,
                    "sha1"=f97c8b779a023996c52fd82b11f5e13be28ecaba,
                    "sha512"=b486ebf21ba6b3465b0fcde98514ca7b841f451e25fe1a8a2c47fa3a6dc61ed80a2ab8d2d8769a8be933567b410651456db6428b5a8c22c3611b0c8a414d08fa,
                )

                $n = $mod.addFile($hashes)
                
                return(
                    $lib.dict(
                        'pnode'=$n.pack(dorepr=$lib.true),
                        'edges'=$n.edges(reverse=$lib.true), 
                        'metasrc_pnode'=$commMod.getMetaSource().pack(dorepr=$lib.true),
                    )
                )
                """
            valu = await core.callStorm(q)

            pnode = valu.get("pnode")
            edges = valu.get("edges")

            # Main node validation
            self.nn(pnode)
            self.eq(
                (
                    "file:bytes",
                    "sha256:dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29baa",
                ),
                s_node.ndef(pnode),
            )
            self.eq("e108f38ff8e45bcc0bd02c084990b6ba", s_node.prop(pnode, "md5"))
            self.eq(
                "f97c8b779a023996c52fd82b11f5e13be28ecaba", s_node.prop(pnode, "sha1")
            )
            self.eq(
                "b486ebf21ba6b3465b0fcde98514ca7b841f451e25fe1a8a2c47fa3a6dc61ed80a2ab8d2d8769a8be933567b410651456db6428b5a8c22c3611b0c8a414d08fa",
                s_node.prop(pnode, "sha512"),
            )

            # only light edge to meta:source should be found
            await self.agenlen(1, edges)
            ledge_node_idens = s_node.iden(valu.get("metasrc_pnode"))
            async for e in edges:
                self.eq(e[0], "seen")
                self.isin(e[1], ledge_node_idens)

            # Validate there are NO file:filepath nodes added
            q = """
                file:filepath +:file=dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29baa
            """
            fpath_nods = await core.nodes(q)
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]
            self.nn(fpath_nods)
            self.len(0, fpath_nods)

    async def test_addFile_optional_hashes(self):
        """
        addFile() with various optional hashes present in the input - always has sha256 - returns file:bytes with specified hashes set; light edge set
        """
        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $commMod = $lib.import(al4.common)
                $mod = $lib.import(al4.ingest)
    
                $hashes = $lib.dict("sha256"=dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29ba7)

                $n = $mod.addFile($hashes)

                return(
                    $lib.dict(
                        'pnode'=$n.pack(dorepr=$lib.true),
                        'edges'=$n.edges(reverse=$lib.true), 
                        'metasrc_pnode'=$commMod.getMetaSource().pack(dorepr=$lib.true),
                    )
                )
                """
            valu = await core.callStorm(q)

            pnode = valu.get("pnode")
            edges = valu.get("edges")

            # Main node validation
            self.nn(pnode)
            self.eq(
                (
                    "file:bytes",
                    "sha256:dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29ba7",
                ),
                s_node.ndef(pnode),
            )
            self.eq(None, s_node.prop(pnode, "md5"))
            self.eq(None, s_node.prop(pnode, "sha1"))
            self.eq(None, s_node.prop(pnode, "sha512"))

            # only light edge to meta:source should be found
            await self.agenlen(1, edges)
            ledge_node_idens = s_node.iden(valu.get("metasrc_pnode"))
            async for e in edges:
                self.eq(e[0], "seen")
                self.isin(e[1], ledge_node_idens)

        async with self.getTestCoreWithPkg() as core:
            q = """ 
                $commMod = $lib.import(al4.common)
                $mod = $lib.import(al4.ingest)
    
                $hashes = $lib.dict(
                    "sha256"=dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29ba7,
                    "sha1"=3128768e981a0bf71d7650fd08a72699bc4ed201
                )

                $n = $mod.addFile($hashes)

                return(
                    $lib.dict(
                        'pnode'=$n.pack(dorepr=$lib.true),
                        'edges'=$n.edges(reverse=$lib.true), 
                        'metasrc_pnode'=$commMod.getMetaSource().pack(dorepr=$lib.true),
                    )
                )
                """
            valu = await core.callStorm(q)

            pnode = valu.get("pnode")
            edges = valu.get("edges")

            # Main node validation
            self.nn(pnode)
            self.eq(
                (
                    "file:bytes",
                    "sha256:dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29ba7",
                ),
                s_node.ndef(pnode),
            )
            self.eq(None, s_node.prop(pnode, "md5"))
            self.eq(
                "3128768e981a0bf71d7650fd08a72699bc4ed201", s_node.prop(pnode, "sha1")
            )
            self.eq(None, s_node.prop(pnode, "sha512"))

            # only light edge to meta:source should be found
            await self.agenlen(1, edges)
            ledge_node_idens = s_node.iden(valu.get("metasrc_pnode"))
            async for e in edges:
                self.eq(e[0], "seen")
                self.isin(e[1], ledge_node_idens)

    async def test_addFile_optional_fileNames(self):
        """
        Validate that file:bytes node is added and file:filepath nodes added
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29baa"
            q = """ 
                $commMod = $lib.import(al4.common)
                $mod = $lib.import(al4.ingest)

                $hashes = $lib.dict(
                    "sha256"=$sha256
                )
                $names = $lib.list(
                    'test.doc',
                    'path/test.doc',
                    $sha256
                )

                yield $mod.addFile($hashes, names=$names)
                """
            nodes = await core.nodes(q, opts={"vars": {"sha256": sha256}})

            self.nn(nodes)
            self.len(1, nodes)
            fnode = nodes[0]

            self.eq(
                fnode.ndef,
                (
                    "file:bytes",
                    f"sha256:{sha256}",
                ),
            )

            # Validate the file:filepath nodes present
            q = """
                file:filepath +:file=$sha256
            """
            fpath_nods = await core.nodes(q, opts={"vars": {"sha256": sha256}})
            ms_node = (await core.nodes('meta:source +:name="usaa-assemblyline4"'))[0]
            self.nn(fpath_nods)
            self.len(2, fpath_nods)

            expected = [
                {
                    "form": "file:filepath",
                    "valu": (f"sha256:{sha256}", "test.doc"),
                },
                {
                    "form": "file:filepath",
                    "valu": (f"sha256:{sha256}", "path/test.doc"),
                },
            ]
            expected_light_edges = [
                ("seen", ms_node.iden()),
            ]

            for nod in fpath_nods:
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

    async def test_addFile_optional_fileType(self):
        """
        Validate that file:bytes node is added with the AL file type
        """
        async with self.getTestCoreWithPkg() as core:
            sha256 = "dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29baa"
            q = """ 
                $commMod = $lib.import(al4.common)
                $mod = $lib.import(al4.ingest)

                $hashes = $lib.dict(
                    "sha256"=$sha256
                )
                $type = "archive/tar"

                yield $mod.addFile($hashes, alFileType=$type)
                """
            nodes = await core.nodes(q, opts={"vars": {"sha256": sha256}})

            self.nn(nodes)
            self.len(1, nodes)
            fnode = nodes[0]

            self.eq(
                fnode.ndef,
                (
                    "file:bytes",
                    f"sha256:{sha256}",
                ),
            )

            self.eq(fnode.props.get("_assemblyline:type"), "archive/tar")

    async def test_addFile_raises_BadArg(self):
        """
        Verify Raises BadArg for improper input param
        """
        async with self.getTestCoreWithPkg() as core:
            # missing sha256 prop in input dict
            q = """ 
                $mod = $lib.import(al4.ingest)
                $inp = $lib.dict('junk'='junk',)
                return($mod.addFile($inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - hashes parameter is missing or invalid.",
                exc.exception.get("mesg"),
            )

            #  null input
            q = """ 
                $mod = $lib.import(al4.ingest)
                $inp = $lib.null
                return($mod.addFile($inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - hashes parameter is missing or invalid.",
                exc.exception.get("mesg"),
            )
