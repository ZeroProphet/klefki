SRC_PATH = ./zkp_playground


dev-install:
	python setup.py develop

test:
	pytest -sv -n auto
debug:
	pytest -sv --pdb
upload:
	python setup.py bdist_wheel
	twine check dist/*
	twine upload dist/*
