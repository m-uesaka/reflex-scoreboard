.PHONY: format test


SRC = abc_scoring_api/
TEST = tests/

format:
	ruff format $(SRC)
	ruff format $(TEST)
	ruff check $(SRC) --fix
	ruff check $(TEST) --fix

test:
	pytest $(TEST)
