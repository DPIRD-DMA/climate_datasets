.PHONY: help sync readme check add update

help:
	@echo "Targets:"
	@echo "  make readme  - regenerate README snapshot from JSON"
	@echo "  make sync    - sync data/datasets.json to docs/data"
	@echo "  make check   - validate README reference labels"
	@echo "  make add     - add dataset (requires JSON on stdin)"
	@echo "  make update  - update dataset (requires NAME and JSON on stdin)"
	@echo "  make all     - run readme + sync + check"

readme:
	@python scripts/generate-readme-table.py

sync:
	@python scripts/sync-dashboard-data.py

check:
	@python scripts/check-reference-labels.py

add:
	@python skills/add-dataset/scripts/add_dataset.py

update:
	@if [ -z "$(NAME)" ]; then echo "NAME is required, e.g., make update NAME=\"SILO\""; exit 1; fi
	@python skills/update-dataset/scripts/update_dataset.py --name "$(NAME)"

all: readme sync check
