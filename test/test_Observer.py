###
# Copyright (c) 2002-2004, Jeremiah Fincher
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

from testsupport import *

class ObserverTestCase(ChannelPluginTestCase):
    plugins = ('Observer', 'Utilities')
    config = {'reply.whenNotCommand': False}
    def tearDown(self):
        g = conf.supybot.plugins.Observer.observers
        L = g()
        for observer in L.copy():
            g.unregister(observer)
            g().remove(observer)
            if observer in g.active():
                g.active().remove(observer)
        super(ObserverTestCase, self).tearDown()

    def testAdd(self):
        self.assertNotError('add foo m/foo/i echo I saw foo.')
        self.assertNoResponse('blah blah blah', 1)
        self.assertNotError('observer enable foo')
        self.assertNoResponse('blah blah blah', 1)
        self.assertResponse('I love to foo!', 'I saw foo.')
        self.assertResponse('Foo you!', 'I saw foo.')
        self.assertResponse('foobar', 'I saw foo.')
        self.assertNotError('observer disable foo')

    def testGroups(self):
        self.assertNotError('add digits m/(\d+)/ echo $1')
        self.assertNoResponse('asdfkjaf', 1)
        self.assertNotError('observer enable digits')
        self.assertNoResponse('asdfkjaf', 1)
        self.assertResponse('abc -- easy as 123', '123')
        self.assertResponse('testing, 1 2 3' , '1')
        self.assertNotError('observer disable digits')

    def testList(self):
        self.assertNotError('add foo m/foo/i echo I saw foo.')
        self.assertRegexp('observer list', 'foo')

    def testInfo(self):
        self.assertNotError('add foo m/foo/i echo I saw foo.')
        self.assertNotRegexp('observer info foo', 'sre')

    def testRemove(self):
        self.assertNotError('add foo m/foo/i echo I saw foo.')
        self.assertRegexp('observer list', 'foo')
        self.assertNotError('observer enable foo')
        self.assertNotError('remove foo')
        self.assertRegexp('observer list', 'no relevant')
        g = conf.supybot.plugins.Observer.observers
        # This works in IRC.  Not sure why it's failing in the test suite
        self.failIf('foo' in conf.get(g.active, self.channel))

    def testObserverWithEmptyGroup(self):
        self.assertNotError('add foo m/foo(bar)?/i echo I saw foo.')
        self.assertNotError('observer enable foo')
        self.assertSnarfRegexp('foo', 'saw foo')

# vim:set shiftwidth=4 tabstop=8 expandtab textwidth=78:

