.PHONY: help sync readme check validate test add update preview all

help:
	@echo "Targets:"
	@echo "  make readme  - regenerate README snapshot from JSON"
	@echo "  make sync    - sync data/datasets.json to docs/data"
	@echo "  make check   - validate README reference labels"
	@echo "  make validate - validate datasets.json structure and URL syntax"
	@echo "  make test    - run dataset skill regression tests"
	@echo "  make add     - add dataset (requires JSON on stdin)"
	@echo "  make update  - update dataset (requires NAME and JSON on stdin)"
	@echo "  make preview - serve docs/ at http://localhost:8000"
	@echo "  make all     - run readme + sync + check + validate + test"

readme:
	@python3 scripts/generate-readme-table.py

sync:
	@python3 scripts/sync-dashboard-data.py

check:
	@python3 scripts/check-reference-labels.py

validate:
	@python3 scripts/validate-datasets.py

test:
	@PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v

add:
	@python3 .agents/skills/add-dataset/scripts/add_dataset.py

update:
	@if [ -z "$(NAME)" ]; then echo "NAME is required, e.g., make update NAME=\"SILO\""; exit 1; fi
	@python3 .agents/skills/update-dataset/scripts/update_dataset.py --name "$(NAME)"

preview:
	@python3 -m http.server -d docs 8000

all: readme sync check validate test
