# GNU  Makefile

PREFIX := $(HOME)/.local/bin

SRC_DIR := src
SRC_RES := $(SRC_DIR)/res
KTREE_DIR := $(HOME)/.ktree
KTREE_RES := $(KTREE_DIR)/res

all:

clean:

install:
	mkdir -p $(PREFIX)
	mkdir -p $(KTREE_DIR)
	mkdir -p $(KTREE_RES)
	install -m 755 $(SRC_DIR)/ktree.py $(PREFIX)/htree
	cp -f $(SRC_RES)/* $(KTREE_RES)/
	cp -f $(SRC_DIR)/viewer.html $(KTREE_DIR)/viewer.html
	@echo "Installed ktree."

uninstall:
	rm -f $(PREFIX)/htree
	rm -rf $(KTREE_DIR)
	@echo "Uninstalled ktree."

.PHONY: install uninstall
