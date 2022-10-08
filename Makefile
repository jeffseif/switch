PYTHON = $(shell which python3)
SHELL = /bin/bash
VENV_DIR = venv

.PHONY: install
install: $(VENV_DIR)

$(VENV_DIR): requirements-minimal.txt
	@$(PYTHON) -m venv $@
	@$@/bin/pip install --quiet --upgrade pip
	@$@/bin/pip install --quiet --requirement=$<

.PHONY: lint
lint: requirements-dev-minimal.txt $(VENV_DIR)
	@$(VENV_DIR)/bin/pip install --quiet --requirement=$<
	@$(VENV_DIR)/bin/pre-commit install
	@$(VENV_DIR)/bin/pre-commit run --all-files

.PHONY: test
test: lint
	@$(VENV_DIR)/bin/pytest tests

.PHONY: clean
clean:
	@git clean -fdfx
