PYTHON=python
TEST_RUNNER=tests/run_tests.py

test:
	$(PYTHON) $(TEST_RUNNER)

test-unit:
	$(PYTHON) $(TEST_RUNNER) --type unit

test-integration:
	$(PYTHON) $(TEST_RUNNER) --type integration

test-podbean:
	$(PYTHON) $(TEST_RUNNER) --type integration --target podbean

test-spotify:
	$(PYTHON) $(TEST_RUNNER) --type unit --target spotify

