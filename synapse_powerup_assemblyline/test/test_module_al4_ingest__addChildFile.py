import logging

import pytest

import synapse.exc as s_exc
import synapse.lib.node as s_node


import test.utils as t_utils

from pprint import pprint

log = logging.getLogger(__name__)


class Module_ingest_Tests(t_utils.TestUtils):
    async def test_addChildFile(self):
        """
        Validate file:bytes node created with all props set; light edge set;
         also validates a file:subfile node is created
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

                $parentSha256 = "b928050b0369bc5fcb396ac0942922e1e03b1200f456d08b7b14c03fb541aeaa"

                $n = $mod.addChildFile($hashes, $parentSha256)
                
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

            q = """
                $commMod = $lib.import(al4.common)
                $mod = $lib.import(al4.ingest)

                file:subfile=(b928050b0369bc5fcb396ac0942922e1e03b1200f456d08b7b14c03fb541aeaa, dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29baa)
                
                return(
                    $lib.dict(
                        'pnode'=$node.pack(dorepr=$lib.true),
                        'edges'=$node.edges(reverse=$lib.true), 
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
                    "file:subfile",
                    (
                        "sha256:b928050b0369bc5fcb396ac0942922e1e03b1200f456d08b7b14c03fb541aeaa",
                        "sha256:dcdc6ec773103d01ec77cc18e4014a907a3c118743191cad71aad3c659e29baa",
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

    async def test_raises_BadArg(self):
        """
        Verify Raises BadArg for improper input param
        """
        async with self.getTestCoreWithPkg() as core:
            # missing sha256 prop in input dict
            q = """ 
                $mod = $lib.import(al4.ingest)
                $inp = $lib.dict('junk'='junk',)
                return($mod.addChildFile($inp, 'junksha256'))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - childFileHashes parameter is missing or invalid.",
                exc.exception.get("mesg"),
            )

            #  null input
            q = """ 
                $mod = $lib.import(al4.ingest)
                $inp = $lib.null
                return($mod.addChildFile($inp, $inp))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - childFileHashes parameter is missing or invalid.",
                exc.exception.get("mesg"),
            )

            #  null input
            q = """ 
                $mod = $lib.import(al4.ingest)
                $inp = $lib.dict('sha256'='1234',)
                return($mod.addChildFile($inp, $lib.null))
                """
            with self.raises(s_exc.BadArg) as exc:
                await core.callStorm(q)
            self.isin(
                "BadArg Exception - parentSha256 parameter is missing or invalid.",
                exc.exception.get("mesg"),
            )
