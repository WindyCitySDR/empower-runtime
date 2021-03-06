#!/usr/bin/env python3
#
# Copyright (c) 2015, Roberto Riggio
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

"""LVNF join event module."""

from empower.core.module import ModuleHandler
from empower.core.module import ModuleWorker
from empower.core.module import Module
from empower.core.module import bind_module
from empower.core.module import handle_callback
from empower.restserver.restserver import RESTServer
from empower.lvnfp.lvnfpserver import LVNFPServer
from empower.lvnfp import PT_LVNF_JOIN

from empower.main import RUNTIME

import empower.logger
LOG = empower.logger.get_logger()


class LVNFJoinHandler(ModuleHandler):
    pass


class LVNFJoin(Module):
    pass


class LVNFJoinWorker(ModuleWorker):
    """LVNFJoin worker."""

    MODULE_NAME = "lvnfjoin"
    MODULE_HANDLER = LVNFJoinHandler
    MODULE_TYPE = LVNFJoin

    def on_lvnf_join(self, lvnf):
        """ Handle an kvnf join event.

        Args:
            lvnf, an LVNF instance

        Returns:
            None
        """

        for event in list(self.modules.values()):

            tenant = RUNTIME.tenants[event.tenant_id]

            if lvnf.lvnf_id not in tenant.lvnfs:
                continue

            LOG.info("Event: LVNF Join %s", lvnf.lvnf_id)

            handle_callback(lvnf, event)


bind_module(LVNFJoinWorker)


def launch():
    """ Initialize the module. """

    lvnf_server = RUNTIME.components[LVNFPServer.__module__]
    rest_server = RUNTIME.components[RESTServer.__module__]

    worker = LVNFJoinWorker(rest_server)
    lvnf_server.register_message(PT_LVNF_JOIN, None, worker.on_lvnf_join)

    return worker
