install:
	install -m 0755 zebu.py $(HOME)/BUILD/bin/zebu
	install -m 0644 zebu.png $(HOME)/BUILD/share/icons/hicolor/48x48/apps/
	install -m 0644 zebu.svg $(HOME)/BUILD/share/icons/hicolor/scalable/apps/

.PHONY: install
