install:
	install -m 0755 zebu.py $(HOME)/BUILD/bin/zebu
	install -m 0644 zebu.desktop $(HOME)/BUILD/share/applications/
	install -m 0644 zebu.svg $(HOME)/BUILD/share/icons/hicolor/scalable/apps/
	install -m 0644 zebu-16.png $(HOME)/BUILD/share/icons/hicolor/16x16/apps/zebu.png
	install -m 0644 zebu-22.png $(HOME)/BUILD/share/icons/hicolor/22x22/apps/zebu.png
	install -m 0644 zebu-32.png $(HOME)/BUILD/share/icons/hicolor/32x32/apps/zebu.png
	install -m 0644 zebu-48.png $(HOME)/BUILD/share/icons/hicolor/48x48/apps/zebu.png

.PHONY: install
