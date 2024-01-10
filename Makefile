.ONESHELL:
pypi:
	# 0. Remove all files from dist/
	rm dist/*

	# 1. Create distribution file
	python setup.py sdist bdist_wheel

	# 2. Upload to Pypi
	twine upload dist/*

format:
	isort -p black euskalmet/*.py
	black -l 100 euskalmet/*.py
	docformatter --wrap-summaries=100 --wrap-descriptions=100 --make-summary-multi-line --pre-summary-newline --in-place  euskalmet/*.py