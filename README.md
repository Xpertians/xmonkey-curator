# XMonkey Curator - Automated DESCAM tooling

## Summary

XMonkey Curator is a tool that perform DESCAM (Decompose, Enumerate, Scanning, Catalog, Analysis, Merge) review to software for Open Source License Compliance.

The tool can extract (Decompose) archive files like Jar, ZIP, Tarballs, RPM, Debian, etc. to recursively obtain the list of assets (Enumerate) contained.

XMonkey Curator also perform basic review (Scanning) to the assets to extract information as "features" that will serve to perform assessments.
Scan types supported:
- Literal Strings
- Regex Patterns (*example*).
- Symbols Matching using predefined *signatures*.

The results of the review can be automatically processed (Catalog) using predefined *rules* and workflows (Analysis).

## Usage

Usage: xmonkey-curator [OPTIONS] PATH

Options:
  -t, --force-text            Force the use of StringExtract for all files.
  -r, --recursive-extraction  Extracting archives files.
  -s, --export-symbols        Include words in the final report.
  -m, --match-symbols         Match symbols against signatures.
  -p, --print-report          Print the report instead of saving to JSON.
  --help                      Show this message and exit.