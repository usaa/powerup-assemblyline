import logging

import test.utils as t_utils


log = logging.getLogger(__name__)


class Module_setup_Tests(t_utils.TestUtils):
    async def test_onload_model_ext(self):
        """
        Verify _assemblyline:type is added to the file:bytes model
        """
        async with self.getTestCoreWithPkg() as core:
            prop = core.model.prop("file:bytes:_assemblyline:type")
            print(prop.pack())
            self.nn(prop)
            self.eq(
                {
                    'name': '_assemblyline:type', 
                    'full': 'file:bytes:_assemblyline:type', 
                    'type': ('str', {'lower': True, 'strip': True}), 
                    'stortype': 1, 
                    'doc': 'Type of file as identified by Assemblyline'
                },
                prop.pack(),
            )
