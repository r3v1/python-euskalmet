.ONESHELL:
pypi:
	# 0. Remove all files from dist/
	rm dist/*

	# 1. Create distribution file
	python setup.py sdist bdist_wheel

	# 2. Upload to Pypi
	# twine upload dist/*
