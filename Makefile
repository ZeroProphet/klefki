SRC_PATH = ./klefki
ASN_PATH = ./asn


dev-install:
	python setup.py develop

test:
	pytest -sv
debug:
	pytest -sv --pdb
asn1:
	asn1ate $(ASN_PATH)/signature.asn > $(SRC_PATH)/asn/signature.py

upload:
	python setup.py bdist_wheel
	twine check dist/*
	twine upload dist/*
