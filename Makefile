SRC_PATH = ./klefki


dev-install:
	python setup.py develop

test:
	pytest -sv
debug:
	pytest -sv --pdb
upload:
	python setup.py bdist_wheel
	twine check dist/*
	twine upload dist/*
