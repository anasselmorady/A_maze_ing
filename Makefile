PYTHON = python3
CONFIG = config.txt

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)
debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
install:
	pip install --upgrade pip
	pip install flake8 mypy build