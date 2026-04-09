
ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

lint:
	uv run ruff check

format:
	uv run ruff fix

run:
	uv run main.py $(RUN_ARGS)
