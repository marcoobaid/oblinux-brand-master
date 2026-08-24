.PHONY: assets validate check-generated clean

assets:
	python3 scripts/generate-assets.py

validate:
	python3 tests/validate.py

check-generated:
	python3 scripts/generate-assets.py --check

clean:
	python3 scripts/generate-assets.py --clean
