.PHONY: help build-ipp build-izg build-all new-subject pages-sync check-html

help:
	@echo "Study guide"
	@echo "  make build-all       IPP + IZG → web/"
	@echo "  make build-ipp       otazky.md → otazky.html + web/ipp/"
	@echo "  make build-izg        otazky.md → otazky.html + web/izg/"
	@echo "  make check-html      ověří Prettier u všech *.html"
	@echo "  make pages-sync      web/ → docs/ (jen pro GitHub Pages)"
	@echo "  make new-subject CODE=IPK TITLE='IPK — Příprava'"

build-all: build-ipp build-izg pages-sync

build-ipp:
	python3 tools/study-guide/build.py IPP

build-izg:
	python3 tools/study-guide/build.py IZG

check-html:
	python3 tools/study-guide/check_html_format.py

pages-sync:
	@rm -rf docs
	@cp -R web docs
	@touch docs/.nojekyll
	@echo "Synced web/ → docs/ (GitHub Pages: folder /docs)"

new-subject:
	@test -n "$(CODE)" && test -n "$(TITLE)" || (echo "Usage: make new-subject CODE=IPK TITLE='IPK — Příprava na zkoušku'"; exit 1)
	python3 tools/study-guide/new_subject.py "$(CODE)" "$(TITLE)" --web
