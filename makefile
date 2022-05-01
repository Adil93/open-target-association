
test:
	@python -m unittest discover -p '*_test.py'

clean:
	@find . -type f -name '*.pyc' -delete

bootstrap:
	@pip install -r requirements.txt

run:
	@python src/app/data_loader.py
	@echo "log file location --> loader.log"
