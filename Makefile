# Program name
NAME = a-maze-ing

# Python
PYTHON = python3

# Main file
MAIN = a_maze_ing.py

# Config file
CONFIG = config.txt

# Colors
GREEN = \033[0;32m
RED = \033[0;31m
RESET = \033[0m

all:
	@echo "$(GREEN)Running $(NAME)...$(RESET)"
	@$(PYTHON) $(MAIN) $(CONFIG)

run:
	@$(PYTHON) $(MAIN) $(CONFIG)

clean:
	@echo "$(RED)Cleaning output...$(RESET)"
	@rm -f maze_output.txt

re: clean all