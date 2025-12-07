# advent_2025

Advent of code, December, 2025

## How I advent of code

I'm running on a Mac. Not tested with any other platform.

The workflow is:

1. `make setup` - needed at the beginning of the contest to set up virtual environment, or if I want to remake it to add/remove/update dependencies.
2. `make jupyter` - start jupyter lab in this virtual environment, and open a terminal in jupyter lab

   I work in jupyter lab which makes it easy to switch over to a notebook if I want to plot something, so my pyproject.toml installs that along with language servers, the vim plugin, and some themes. However, most of the time I just work in .py files.
4. `make get-day-X` (for example: *`make get-day-1`*) - download the problem
5. `make sample-day-X` - download example problem.
6. `cd` *`day-dir`* - cd into the day's directory
7. `python watch.py` - run the work-in-progress file `wip.py` in a loop

   When the first part is solved, I copy `wip.py` to `part1.py` so I can edit for part 2 without losing my solution for part 1.

Makefile is self-documenting.  Run `make help`

### Prerequisites

Requires uv.  See [instructions](https://docs.astral.sh/uv/getting-started/installation/)

### Problem download notes

The pyproject.toml installs [advent-of-code-data](https://github.com/wimglenn/advent-of-code-data) to download the problem example as
well as my personal input.

- `make get-day-X` - download the input and example for day X in a new subdirectory by day.  Will not overwrite existing files.
- `make sample-day-X` - download the example problem for day X. **Will** overwrite existing file, since the answer for part 2 is not revealed until part 1 is submitted.

The "get" rule copies `wip.py` and `watch.py` from the top level into the new day's subdirectory for development.  The work-in-progress file is always edited. The watcher may need to be edited if my solution is spread over more than one file.

The "sample" file includes header and footer information and will need to be copied and editied. The `wip` file expects this copy to be saved as `input-sample.txt`

### Problem solving

`watch.py` will re-run the `wip.py` file on each save. It uses [watchfiles](https://github.com/samuelcolvin/watchfiles)

The following tools are used in `wip.py`

- [pytest](https://docs.pytest.org/) -- I have a stub test set up to test that the sample data returns the sample result. I can add additional tests simply by adding a function named test_XXX. The `solve` function is not run on the personal input until the sample test passes.
- [icecream](https://github.com/gruns/icecream) -- Debugging with print statements is often the way to go for quick-checking different steps of the puzzle. These print statements run during the test phase and are turned off when the personal input is processed.
- [parse](https://github.com/r1chardj0n3s/parse) -- Text parse library that comes in handy sometimes.  Does a little more than `str.split()` and a little less fancy but easier to use than `re`.
- [pandas](https://pandas.pydata.org) and [numpy](https://numpy.org) just-in-case imports that I find handy.

### Pre-commit

Pre-commit is not turned on too strict. It's throwaway code, but it's nice to keep things formatted and remove unused code or imports when all done.
