.PHONY: help sync readme check validate add update preview

help:
	@echo "Targets:"
	@echo "  make readme  - regenerate README snapshot from JSON"
	@echo "  make sync    - sync data/datasets.json to docs/data"
	@echo "  make check   - validate README reference labels"
	@echo "  make validate - validate datasets.json structure and URLs"
	@echo "  make add     - add dataset (requires JSON on stdin)"
	@echo "  make update  - update dataset (requires NAME and JSON on stdin)"
	@echo "  make preview - serve docs/ at http://localhost:8000"
	@echo "  make all     - run readme + sync + check + validate"

readme:
	@python scripts/generate-readme-table.py

sync:
	@python scripts/sync-dashboard-data.py

check:
	@python scripts/check-reference-labels.py

validate:
	@python scripts/validate-datasets.py

add:
	@python skills/add-dataset/scripts/add_dataset.py

update:
	@if [ -z "$(NAME)" ]; then echo "NAME is required, e.g., make update NAME=\"SILO\""; exit 1; fi
	@python skills/update-dataset/scripts/update_dataset.py --name "$(NAME)"

preview:
	@python -m http.server -d docs 8000

all: readme sync check validate
