test:
	PYTHONPATH=.. python3 -m pytest -v

unit_test:
	PYTHONPATH=.. python3 -m pytest -v -m "not perf"

perf_test:
	PYTHONPATH=.. python3 -m pytest -v -s -m "perf"

lint:
	python3 -m ruff check ..

coverage:
	PYTHONPATH=.. python3 -m coverage run --source=.. --omit="tests/*" -m pytest
	python3 -m coverage report
	python3 -m coverage html

doc:
	PYTHONPATH=.. python3 -m pdoc --html --output-dir docs --force ../api.py ../point_set.py ../triangulator.py
