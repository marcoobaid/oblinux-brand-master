.PHONY: assets wallpapers validate check-generated clean

assets:
	python3 scripts/generate-assets.py

# Authoring only: re-export released production wallpapers; update their pinned
# SHA-256 in tests/validate.py in the same change. Package builds never run this.
wallpapers:
	python3 scripts/generate-assets.py --wallpapers

validate:
	python3 tests/validate.py

check-generated:
	python3 scripts/generate-assets.py --check

clean:
	python3 scripts/generate-assets.py --clean
