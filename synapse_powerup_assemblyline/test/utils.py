import contextlib
import logging
import os
import json
from datetime import datetime

import pytest
import synapse.common as s_common
import synapse.cortex as s_cortex
import synapse.tools.genpkg as s_genpkg

import synapse.tests.utils as s_test

log = logging.getLogger(__name__)

DATE_TIME_FMT = "%Y-%m-%d %H:%M:%S"


dirname = s_common.genpath(
    os.path.dirname(__file__), "../src",
)


class TestUtils(s_test.StormPkgTest):
    assetdir = s_common.genpath(os.path.dirname(__file__), "testassets")
    pkgprotos = (os.path.join(dirname, "package.yml"),)

    @contextlib.asynccontextmanager
    async def getTestCoreWithPkg(self):
        """
        Get a test Core with the Assemblyline Package already loaded
        """
        async with self.getTestCore() as core:
            yield core

    def getTestFileJson(self, name):
        with open(self.getTestFilePath(name), "r") as f:
            return json.load(f)

    def getTestFileJsonAsRawOntologyResult(self, name):
        with open(self.getTestFilePath(name), "r") as f:
            ontDict = json.load(f)
            output = ""
            for item in ontDict:
                output = output + json.dumps(item) + "\n"
            return output

    # overriding
    def getTestFilePath(self, *names):
        import test.__init__

        path = os.path.dirname(test.__init__.__file__)
        return os.path.join(path, "testassets", *names)

    def fmtDateStr(self, ts: int) -> str:
        dt = datetime.datetime.fromtimestamp(ts / 1e3)
        return dt.strftime(DATE_TIME_FMT)
