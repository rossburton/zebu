# Copyright (C) 2008 Ross Burton <ross@burtonini.com>
#
# Zebu is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# Zebu is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Zebu.  If not, see <http://www.gnu.org/licenses/>.

import gobject, gtk

distros = {
    "debian": ("http://ftp.uk.debian.org/debian", "main"),
    "ubuntu": ("http://archive.ubuntu.com/ubuntu", "main universe")
    }
releases = (
    ("Debian Unstable (Sid)", "debian", "unstable"),
    ("Debian Testing (Lenny)", "debian", "lenny"),
    ("Debian 4.0 (Etch)", "debian", "etch"),
    ("Debian 3.1 (Sarge)", "debian", "sarge"),
    ("Ubuntu 8.10 (Intrepid Ibex)", "ubuntu", "intrepid"),
    ("Ubuntu 8.04 (Hardy Heron)", "ubuntu", "hardy"),
    ("Ubuntu 7.10 (Gutsy Gibbon)", "ubuntu", "gutsy"),
    ("Ubuntu 7.04 (Feisty Fawn)", "ubuntu", "feisty"),
    ("Ubuntu 6.10 (Edgy Eft)", "ubuntu", "edgy"),
    ("Ubuntu 6.06 (Dapper Drake)", "ubuntu", "dapper"),
)

class NewCowDialog(gtk.Dialog):
    def __init__(self, parent=None):
        gtk.Dialog.__init__(self, "Create New Cowbuilder", parent)
        self.set_resizable(False)
        
        def make_label(text):
            label = gtk.Label()
            label.set_markup_with_mnemonic("<b>%s</b>" % text)
            label.set_alignment(1.0, 0.5)
            label.show()
            return label

        table = gtk.Table(3, 2)
        table.set_row_spacings(6)
        table.set_col_spacings(6)
        table.set_border_width(4)
        table.show()
        self.vbox.add(table)

        label = make_label("_Name:")
        table.attach(label, 0, 1, 0, 1)

        self.name_entry = entry = gtk.Entry()
        entry.show()
        table.attach(entry, 1, 2, 0, 1)
        label.set_mnemonic_widget(entry)
        
        label = make_label("_Distribution:")
        table.attach(label, 0, 1, 1, 2)

        # Label, mirror, release, components, 
        store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
        for release in releases:
            distro = distros[release[1]]
            store.set(store.append(),
                      0, release[0],
                      1, distro[0],
                      2, release[2],
                      3, distro[1])

        self.distro_combo = combo = gtk.ComboBox(store)
        renderer = gtk.CellRendererText()
        combo.pack_start(renderer)
        combo.add_attribute(renderer, "text", 0)
        combo.set_active(0)
        combo.show()
        table.attach(combo, 1, 2, 1, 2)
        label.set_mnemonic_widget(combo)

        self.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                         gtk.STOCK_NEW, gtk.RESPONSE_ACCEPT)

    def get_name(self):
        return self.name_entry.get_text()

    def get_details(self):
        """Return a (mirror, release, components) tuple"""
        model = self.distro_combo.get_model()
        it = self.distro_combo.get_active_iter()

        if it:
            return model.get(it, 1, 2, 3)
        else:
            return None

if __name__ == "__main__":
    dialog = NewCowDialog()
    if dialog.run() == gtk.RESPONSE_ACCEPT:
        print dialog.get_name()
        print dialog.get_details()
