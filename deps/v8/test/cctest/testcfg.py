# Copyright 2008 the V8 project authors. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of Google Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import shutil

from testrunner.local import commands
from testrunner.local import testsuite
from testrunner.local import utils
from testrunner.objects import testcase


class CcTestSuite(testsuite.TestSuite):
  SHELL = 'cctest'

  def __init__(self, name, root):
    super(CcTestSuite, self).__init__(name, root)
    if utils.IsWindows():
      build_dir = "build"
    else:
      build_dir = "out"

  def ListTests(self, context):
    shell = os.path.abspath(os.path.join(context.shell_dir, self.SHELL))
    if utils.IsWindows():
      shell += ".exe"
    cmd = context.command_prefix + [shell, "--list"] + context.extra_flags
    output = commands.Execute(cmd)
    if output.exit_code != 0:
      print ' '.join(cmd)
      print output.stdout
      print output.stderr
      return []
    tests = []
    for test_desc in output.stdout.strip().split():
      test = testcase.TestCase(self, test_desc)
      tests.append(test)
    tests.sort(key=lambda t: t.path)
    return tests

  def GetShellForTestCase(self, testcase):
    return self.SHELL

  def GetParametersForTestCase(self, testcase, context):
    return [testcase.path], testcase.flags + context.mode_flags, {}


def GetSuite(name, root):
  return CcTestSuite(name, root)
