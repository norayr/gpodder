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

import gtk

import gpodder

_ = gpodder.gettext

from gpodder.gtkui.interface.common import BuilderWidget

from gpodder import util


class gPodderAddPodcast(BuilderWidget):
    finger_friendly_widgets = ['btn_close', 'btn_add' 'btn_paste']

    def new(self):
        if not hasattr(self, 'add_urls_callback'):
            self.add_urls_callback = None
        if hasattr(self, 'custom_label'):
            self.label_add.set_text(self.custom_label)
        if hasattr(self, 'custom_title'):
            self.gPodderAddPodcast.set_title(self.custom_title)
        if hasattr(self, 'preset_url'):
            self.entry_url.set_text(self.preset_url)
        self.entry_url.connect('activate', self.on_entry_url_activate)
        if gpodder.ui.fremantle:
            self.btn_add = self.main_window.add_button(gtk.STOCK_ADD, 0)
            self.btn_add.connect('clicked', self.on_btn_add_clicked)
            self.on_entry_url_changed(self.entry_url) # for sensitivity
            self.btn_add.show_all()
            # Deactivate capitalization and word completion (Maemo bug 5184)
            self.entry_url.set_property('hildon-input-mode', \
                    gtk.HILDON_GTK_INPUT_MODE_FULL)
        elif gpodder.ui.diablo:
            self.entry_url.set_property('hildon-input-mode', \
                    'HILDON_GTK_INPUT_MODE_FULL')
        self.gPodderAddPodcast.show()

        if not hasattr(self, 'preset_url'):
            # Fill the entry if a valid URL is in the clipboard, but
            # only if there's no preset_url available (see bug 1132)
            clipboard = gtk.Clipboard(selection='PRIMARY')
            def receive_clipboard_text(clipboard, text, second_try):
                if text is not None:
                    url = util.normalize_feed_url(text)
                    if url is not None:
                        self.entry_url.set_text(url)
                        self.entry_url.set_position(-1)
                        return

                if not second_try:
                    clipboard = gtk.Clipboard()
                    clipboard.request_text(receive_clipboard_text, True)
            clipboard.request_text(receive_clipboard_text, False)

    def on_btn_close_clicked(self, widget):
        self.gPodderAddPodcast.destroy()

    def on_btn_paste_clicked(self, widget):
        clipboard = gtk.Clipboard()
        clipboard.request_text(self.receive_clipboard_text)

    def receive_clipboard_text(self, clipboard, text, data=None):
        if text is not None:
            self.entry_url.set_text(text)
        else:
            self.show_message(_('Nothing to paste.'), _('Clipboard is empty'))

    def on_entry_url_changed(self, widget):
        self.btn_add.set_sensitive(self.entry_url.get_text().strip() != '')

    def on_entry_url_activate(self, widget):
        self.on_btn_add_clicked(widget)

    def on_btn_add_clicked(self, widget):
        url = self.entry_url.get_text()
        self.on_btn_close_clicked(widget)
        if self.add_urls_callback is not None:
            self.add_urls_callback([url])

