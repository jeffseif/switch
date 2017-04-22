PYTHON = $(shell which python3)
VENV = venv/

.PHONY: all
all: install

.PHONY: install
install: $(VENV).setup

$(VENV).setup: $(VENV)
	@$</bin/python setup.py \
		install \
		--quiet
	@touch $@

$(VENV): requirements.txt
	@virtualenv \
		--no-site-packages \
		--python=$(PYTHON) \
		$@
	@$@/bin/pip install \
		--requirement $<
	@$@/bin/pip install \
		--upgrade pip
	@touch $@

.PHONY: test
test: $(VENV)
	@$</bin/tox

.PHONY: clean
clean:
	@$(VENV)bin/python setup.py clean --all
	@rm -rf *.egg-info/
	@rm -rf .cache/
	@rm -rf .eggs/
	@rm -rf .tox/
	@rm -rf dist/
	@rm -rf .pytest_cache/
	@rm -f .coverage
	@rm -rf $(VENV)
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -delete
