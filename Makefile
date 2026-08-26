install:
	python3 -m venv env
	env/bin/python -m pip install -r requirements.txt
	@echo "To activate environment: $ source env/bin/activate"

run:
	python3 fly_in.py
