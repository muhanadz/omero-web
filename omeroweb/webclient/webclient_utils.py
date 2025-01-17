#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (C) 2011 University of Dundee & Open Microscopy Environment.
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import datetime

logger = logging.getLogger(__name__)


def getDateTime(timeString):
    return datetime.datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S")


def formatPercentFraction(value):
    """Formats a fraction as a percentage for display"""
    value = value * 100
    if value < 1:
        # Handle python3 rounding 0.05 towards even numbers
        # Make sure it always rounds 0.05 up
        if (value * 10) % 1 == 0.5:
            value += 0.01
        value = "%.1f" % round(value, 1)
    else:
        # Make sure it always rounds 0.5 up
        if value % 1 == 0.5:
            value += 0.1
        value = "%s" % int(round(value))
    return value


def _formatReport(callback):
    """
    Added as workaround to the changes made in #3006.
    """
    rsp = callback.getResponse()
    if not rsp:
        return  # Unfinished

    import omero

    if isinstance(rsp, omero.cmd.ERR):
        err = rsp.parameters.get("Error", "")
        warn = rsp.parameters.get("Warning", "")
        logger.error("Format report: %r" % {"error": err, "warning": warn})
        return "Operation could not be completed successfully"
    # Delete2Response, etc include no warnings
    # Might want to take advantage of other feedback here


def _purgeCallback(request, limit=200):

    callbacks = request.session.get("callback", {}).keys()
    if len(callbacks) > limit:
        cbKeys = list(request.session.get("callback").keys())
        for (cbString, count) in zip(cbKeys, range(0, len(callbacks) - limit)):
            del request.session["callback"][cbString]
