YEAR = 2025

# From https://gist.github.com/prwhite/8168133
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

setup: ## Sets up jupyter, aoc, template, etc. using uv
	uv sync
	uv run npm install -g --prefix ./.venv bash-language-server pyright sql-language-server unified-language-server vscode-json-languageserver-bin yaml-language-server
	uv run pre-commit install

jupyter: ## Start jupyter alb
	uv run jupyter lab

clean: ## Blow away venv to start over
	rm -r .venv

get-day-%: ## Get input for day % (will not overwrite files)
	$(eval directory := $(shell printf %02d $(@:get-day-%=%)))
	test -d $(directory) || mkdir $(directory)
	test -f $(directory)/input.py || uv run aocd $(@:get-day-%=%) $(YEAR) > $(directory)/input.txt
	test -f $(directory)/watcher.py || cp watcher.py $(directory)
	test -f $(directory)/wip.py || cp wip.py $(directory)


sample-day-%: ## See sample for day % (will overwrite example.txt, to pick up example solution in part2 once part1 is done)
	$(eval directory := $(shell printf %02d $(@:sample-day-%=%)))
	test -d $(directory) || mkdir $(directory)
	uv run aocd $(@:sample-day-%=%) $(YEAR) --example | tee  $(directory)/example.txt
