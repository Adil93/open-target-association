test:
	@export PYTHONPATH=`pwd`/src; python -m unittest discover -p '*_test.py'

clean:
	@find . -type f -name '*.pyc' -delete

bootstrap:
	@pip install -r requirements.txt
	

run:
	@export PYTHONPATH=`pwd`/src; python src/app/data_loader.py
	@echo "log file location --> loader.log"
