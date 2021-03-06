"""The unittest.TestCase for FSM workloads."""

from __future__ import absolute_import

import os.path
import threading

from buildscripts.resmokelib.testing.testcases import jsrunnerfile


class FSMWorkloadTestCase(jsrunnerfile.JSRunnerFileTestCase):
    """An FSM workload to execute."""

    REGISTERED_NAME = "fsm_workload_test"

    _COUNTER_LOCK = threading.Lock()
    _COUNTER = 0

    def __init__(self, logger, fsm_workload, shell_executable=None, shell_options=None):
        """Initialize the FSMWorkloadTestCase with the FSM workload file."""

        jsrunnerfile.JSRunnerFileTestCase.__init__(
            self, logger, "FSM workload", fsm_workload,
            test_runner_file="jstests/concurrency/fsm_libs/resmoke_runner.js",
            shell_executable=shell_executable, shell_options=shell_options)

    @property
    def fsm_workload(self):
        """Get the test name."""
        return self.test_name

    def _populate_test_data(self, test_data):

        test_data["fsmWorkloads"] = self.fsm_workload

        with FSMWorkloadTestCase._COUNTER_LOCK:
            count = FSMWorkloadTestCase._COUNTER
            FSMWorkloadTestCase._COUNTER += 1

        # We use a global incrementing counter as a prefix for the database name to avoid any
        # collection lifecycle related issues in sharded clusters. This more closely matches how
        # uniqueDBName() and uniqueCollName() would have returned distinct values when called once
        # for each FSM workload in the entire schedule by runner.js.
        test_data["dbNamePrefix"] = "test{:d}_".format(count)
