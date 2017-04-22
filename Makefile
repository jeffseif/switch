.PHONY: all
all: install

.PHONY: install
install: venv/.setup

venv/.setup: venv
	@$</bin/python setup.py \
		install \
		--quiet
	@touch $@

venv: requirements.txt
	@virtualenv \
		--no-site-packages \
		--python=$(which python3) \
		$@
	@$@/bin/pip install \
		--requirement $<
	@$@/bin/pip install \
		--upgrade pip
	@touch $@

.PHONY: test
test: venv
	@$</bin/tox

.PHONY: clean
clean:
	@venv/bin/python setup.py clean --all
	@rm -rf *.egg-info/
	@rm -rf .cache/
	@rm -rf .eggs/
	@rm -rf .tox/
	@rm -rf dist/
	@rm -f .coverage
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -delete
