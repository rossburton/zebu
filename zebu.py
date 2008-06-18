#! /usr/bin/python

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

import gobject, gtk, os, re

gtk.window_set_default_icon_name("zebu")

window = gtk.Window()
window.set_title("Zebu Cowbuilder Manager")
window.set_default_size(300, 250)
window.set_border_width(8)
window.connect("delete-event", gtk.main_quit)

vbox = gtk.VBox(spacing=8)
window.add(vbox)

scrolled = gtk.ScrolledWindow()
scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
scrolled.set_shadow_type(gtk.SHADOW_IN)

# Full path, short name, description
(COL_PATH,
 COL_NAME,
 COL_DESC) = range(0, 3)
store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
store.set_sort_column_id(COL_NAME, gtk.SORT_ASCENDING)

treeview = gtk.TreeView(store)
column = gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=COL_NAME)
treeview.append_column(column)
column = gtk.TreeViewColumn("Description", gtk.CellRendererText(), text=COL_DESC)
treeview.append_column(column)
scrolled.add(treeview)
vbox.pack_start(scrolled)

def sync_selection(selection, button):
    """
    Set the sensitivity of a button based on the treeview selection.
    """
    button.set_sensitive(selection.count_selected_rows() != 0)

def spawn_cowbuilder(option):
    (model, it) = treeview.get_selection().get_selected()
    row = model[it]
    args = (
        "gnome-terminal",
        "-t", "Cowshell in %s" % row[COL_NAME],
        "-x", "sudo", "sh", "-c",
        "cowbuilder %s --basepath %s ; read -n 1 -p '[done, press any key]'" % (option, row[COL_PATH])
        )
    gobject.spawn_async(argv=args, flags=gobject.SPAWN_SEARCH_PATH)

bbox = gtk.HButtonBox()

button = gtk.Button("Update");
def on_update_clicked(button):
    spawn_cowbuilder("--update")
button.connect("clicked", on_update_clicked)
treeview.get_selection().connect("changed", sync_selection, button)
bbox.add(button)

button = gtk.Button("Login")
def on_login_clicked(button):
    spawn_cowbuilder("--login")
button.connect("clicked", on_login_clicked)
treeview.get_selection().connect("changed", sync_selection, button)
bbox.add(button)

vbox.pack_start(bbox, expand=False)


COW_DIR = "/var/cache/pbuilder"
for name in os.listdir(COW_DIR):
    if not name.endswith(".cow"):
        continue

    path = os.path.join(COW_DIR, name)
    if not os.path.isdir(path):
        continue

    desc = ""
    try:
        lsbre = re.compile(r'DISTRIB_DESCRIPTION="(.+)"')
        for l in open(os.path.join(path, "etc", "lsb-release")):
            m = lsbre.match(l)
            if m:
                desc = m.group(1)
                break;
    except IOError:
        pass
    
    if not desc:
        try:
            deb_version = open(os.path.join(path, "etc", "debian_version")).readline().strip()
            desc = "Debian %s" % deb_version
        except IOError:
            pass
    
    store.set(store.append(),
              COL_PATH, path,
              COL_NAME, name,
              COL_DESC, desc)

window.show_all()
gtk.main()
