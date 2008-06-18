#! /usr/bin/python

import gobject, gtk, os, re

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
store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
store.set_sort_column_id(1, gtk.SORT_ASCENDING)

treeview = gtk.TreeView(store)
column = gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=1)
treeview.append_column(column)
column = gtk.TreeViewColumn("Description", gtk.CellRendererText(), text=2)
treeview.append_column(column)
scrolled.add(treeview)
vbox.pack_start(scrolled)

def spawn(command):
    title = "Cowshell" #in %s" % model[it][1]
    args = (command % (title, model[it][0])).split(" ")
    gobject.spawn_async(argv=args, flags=gobject.SPAWN_SEARCH_PATH)

def spawn_cowbuilder(option):
    (model, it) = treeview.get_selection().get_selected()
    row = model[it]
    args = (
        "gnome-terminal",
        "-t", "'Cowshell in %s'" % row[1],
        "-x", "sudo", "sh", "-c",
        "cowbuilder %s --basepath %s ; read -n 1 -p '[done, press any key]'" % (option, row[0])
        )
    gobject.spawn_async(argv=args, flags=gobject.SPAWN_SEARCH_PATH)

bbox = gtk.HButtonBox()

button = gtk.Button("Update");
def on_update_clicked(button):
    spawn_cowbuilder("--update")
button.connect("clicked", on_update_clicked)
bbox.add(button)

button = gtk.Button("Login")
def on_login_clicked(button):
    spawn_cowbuilder("--login")
button.connect("clicked", on_login_clicked)
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
    
    store.set(store.append(), 0, path, 1, name, 2, desc)

window.show_all()
gtk.main()
