# -*- coding: utf-8 -*-
#
# gPodder - A media aggregator and podcast client
# Copyright (c) 2005-2010 Thomas Perl and the gPodder Team
#
# gPodder is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# gPodder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
# gpodder.player - Podcatcher implementation of the Media Player D-Bus API
# Thomas Perl <thp@gpodder.org>; 2010-04-25
#
# Specification: http://gpodder.org/wiki/Media_Player_D-Bus_API
#


try:
    import dbus
except ImportError:
    # Import Mock D-Bus interfaces when D-Bus bindings are not installed
    from gpodder.gui import dbus

import gpodder

class MediaPlayerDBusReceiver(object):
    INTERFACE = 'org.gpodder.player'
    SIGNAL_STARTED = 'PlaybackStarted'
    SIGNAL_STOPPED = 'PlaybackStopped'

    def __init__(self, on_play_event):
        self.on_play_event = on_play_event

        self.bus = gpodder.dbus_session_bus
        self.bus.add_signal_receiver(self.on_playback_started, \
                                     self.SIGNAL_STARTED, \
                                     self.INTERFACE, \
                                     None, \
                                     None)
        self.bus.add_signal_receiver(self.on_playback_stopped, \
                                     self.SIGNAL_STOPPED, \
                                     self.INTERFACE, \
                                     None, \
                                     None)

    def on_playback_started(self, position, file_uri):
        pass

    def on_playback_stopped(self, start, end, total, file_uri):
        if file_uri.startswith('/'):
            file_uri = 'file://' + file_uri
        self.on_play_event(start, end, total, file_uri)

