install:
	python setup.py install --user

uninstall:
	pip uninstall kutty -y

clean:
	rm -rf build dist *.egg-info
	rm -rf kutty/__pycache__ kutty/*/__pycache__ kutty/*/*/__pycache__
	rm -rf kutty/*/*.pyc kutty/*/*/*.pyc

lint:
	pylint kutty --disable=missing-docstring