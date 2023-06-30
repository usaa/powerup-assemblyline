import logging

import pytest

import synapse.exc as s_exc

import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_Security__AL4_PRIVSEP__Tests(t_utils.TestUtils):
    async def test_importmodule_by_NonUser_raises_AuthDeny_noAsRootPerms(self):
        """
        Try to import al4.privsep and verify Raises AuthDeny for a user that does not
        have asRoot permissions.
        i.e. user must be a member of power-ups.al4.user
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.privsep)
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_importmodule_by_user_works(self):
        """
        Verify user that is a member of power-ups.al4.user is able to import the module
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.privsep)
                return($mod.getTagPrefix())
                """
                valu = await asuser.callStorm(q)
                self.nn(valu)


class Module_Security__AL4_SETUP_ADMIN__Tests(t_utils.TestUtils):
    async def test_importmodule_by_NonUser_raises_AuthDeny_noAsRootPerms(self):
        """
        Try to import al4.setup.admin and verify Raises AuthDeny for a user that does not
        have asRoot permissions.
        i.e. user must be a member of power-ups.al4.admin
        """
        async with self.getTestCoreWithPkg() as core:
            await core.auth.addUser("user")

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

        """
        Verify user that is a member of power-ups.al4.user also fails
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                """
                await self.asyncraises(s_exc.AuthDeny, asuser.callStorm(q))

    async def test_importmodule_by_admin_works(self):
        """
        Verify user that is a member of power-ups.al4.admin is able to import the module
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "admin")))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup.admin)
                return($mod.getGlobalTagPrefix())
                """
                valu = await asuser.callStorm(q)
                self.none(valu)


class Module_Security__ALLOTHERMODULES__Tests(t_utils.TestUtils):
    """
    Validate that all other modules are able to be imported by a standard user.
    """

    async def test_importmodule_AL4COMMON_by_basicuser_with_no_perms_works(self):
        """
        # module: al4.common
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.common)
                return($lib.true)
                """
                valu = await asuser.callStorm(q)
                self.true(valu)

    async def test_importmodule_AL4INGEST_by_basicuser_with_no_perms_works(self):
        """
        # module: al4.ingest
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.ingest)
                return($lib.true)
                """
                valu = await asuser.callStorm(q)
                self.true(valu)

    async def test_importmodule_AL4ONTOLOGY_by_basicuser_with_no_perms_works(self):
        """
        # module: al4.ontology
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.ontology)
                return($lib.true)
                """
                valu = await asuser.callStorm(q)
                self.true(valu)

    async def test_importmodule_AL4ONTOLOGYV1X_by_user_with_user_perms_works(self):
        """
        # module: al4.ontology.v1x
        # Even though the package def does not require a permission, the package still
        #  imports al4.privsep which does require power-ups.al4.user perms.
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.ontology.v1x)
                return($lib.true)
                """
                valu = await asuser.callStorm(q)
                self.true(valu)

    async def test_importmodule_AL4SETUP_by_basicuser_with_no_perms_works(self):
        """
        # module: al4.setup
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4.setup)
                return($lib.true)
                """
                valu = await asuser.callStorm(q)
                self.true(valu)

    async def test_importmodule_AL4_by_user_with_perms_works(self):
        """
        # module: al4
        # Even though the package def does not require a permission, the package still
        #  imports al4.privsep which does require power-ups.al4.user perms.
        """
        async with self.getTestCoreWithPkg() as core:
            user = await core.auth.addUser("user")
            await user.addRule((True, ("power-ups", "al4", "user")))
            await user.addRule((True, ("node",)))

            async with core.getLocalProxy(user="user") as asuser:
                q = """
                $mod = $lib.import(al4)
                return($lib.true)
                """
                valu = await asuser.callStorm(q)
                self.true(valu)
