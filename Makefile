format:
	ruff --fix .

test:
	python3 test.py

start:
	python main.py

truncate-file:
	truncate -s 0 logs/test.py.log
	truncate -s 0 logs/get_records.py.log
	truncate -s 0 logs/table.py.log
