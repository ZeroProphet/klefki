SRC_PATH = ./klefki
ASN_PATH = ./asn


dev-install:
	python setup.py develop

test:
	pytest

asn1:
	asn1ate $(ASN_PATH)/signature.asn > $(SRC_PATH)/asn/signature.py
