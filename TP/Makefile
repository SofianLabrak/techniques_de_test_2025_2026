test:
	PYTHONPATH=.. pytest -v

unit_test:
	PYTHONPATH=.. pytest -v -m "not perf"

perf_test:
	PYTHONPATH=.. pytest -v -s -m "perf"

lint:
	ruff check ..

coverage:
	PYTHONPATH=.. coverage run --source=.. --omit="tests/*" -m pytest
	coverage report
	coverage html

doc:
	PYTHONPATH=.. pdoc --html --output-dir docs --force ../api.py ../point_set.py ../triangulator.py
