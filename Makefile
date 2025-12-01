YEAR = 2025

# From https://gist.github.com/prwhite/8168133
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

setup: ## Sets up jupyter, aoc, template, etc. using uv
	uv sync
	uv run npm install -g --prefix ./.venv bash-language-server pyright sql-language-server unified-language-server vscode-json-languageserver-bin yaml-language-server
	uv run npm install -g --prefix ./.venv  @jakzo/aoc
	cp wip.py .venv/lib/node_modules/\@jakzo/aoc/templates/python
	uv run pre-commit install

jupyter: ## Start jupyter alb
	uv run jupyter lab

clean: ## Blow away venv to start over
	rm -r .venv


get-day-%: ## Print the problem for day "%" and wait for answers
	uv run aoc -y $(YEAR) -d $(@:get-day-%=%)

solve-day-%: ## Start solving day "%"
	uv run aoc start -y $(YEAR) -d $(@:solve-day-%=%) python
