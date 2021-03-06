#!/usr/bin/env python3
#
# Copyright (c) 2016, Roberto Riggio
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the CREATE-NET nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY CREATE-NET ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CREATE-NET BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Counters Poller Apps."""

from empower.apps.pollers.poller import Poller
from empower.apps.pollers.poller import DEFAULT_POLLING
from empower.core.app import DEFAULT_PERIOD
from empower.events.lvapjoin import lvapjoin
from empower.counters.packets_counter import packets_counter
from empower.counters.bytes_counter import bytes_counter

import empower.logger
LOG = empower.logger.get_logger()


class CountersPoller(Poller):
    """Counters Poller Apps.

    Command Line Parameters:

        period: loop period in ms (optional, default 5000ms)

    Example:

        ID="52313ecb-9d00-4b7d-b873-b55d3d9ada26"
        ./empower-runtime.py apps.pollers.counterspoller:$ID

    """

    def __init__(self, tenant, **kwargs):

        Poller.__init__(self, tenant, **kwargs)

        lvapjoin(tenant_id=self.tenant.tenant_id,
                 callback=self.lvap_join_callback)

    def lvap_join_callback(self, lvap):
        """ New LVAP. """

        packets_counter(bins=[512, 1472, 8192],
                        lvap=lvap.addr,
                        tenant_id=self.tenant.tenant_id,
                        every=self.polling,
                        callback=self.packets_callback)

        bytes_counter(bins=[512, 1472, 8192],
                      lvap=lvap.addr,
                      tenant_id=self.tenant.tenant_id,
                      every=self.polling,
                      callback=self.bytes_callback)

    def packets_callback(self, stats):
        """ New stats available. """

        LOG.info("New stats (packets) received from %s" % stats.lvap)

    def bytes_callback(self, stats):
        """ New stats available. """

        LOG.info("New stats (bytes) received from %s" % stats.lvap)


def launch(tenant,
           filepath="./",
           polling=DEFAULT_POLLING,
           period=DEFAULT_PERIOD):
    """ Initialize the module. """

    return CountersPoller(tenant,
                          filepath=filepath,
                          polling=polling,
                          every=period)
