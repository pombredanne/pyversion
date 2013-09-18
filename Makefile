.PHONY: style-check test

style-check:
	flake8 --max-complexity 6 ./semver/

test:
	python3 -m unittest --verbose --catch --failfast tests.py

clean:
	@rm -rv ./{pyversion/,}__pycache__/
