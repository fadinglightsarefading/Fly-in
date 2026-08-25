install:
	python3 -m venv fly_in_env
	fly_in_env/bin/python -m pip install -r requirements.txt

run:
	python3 fly_in.py
