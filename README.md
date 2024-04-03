# XMonkey Curator - Automated DESCAM tooling

## Summary

XMonkey Curator is a tool that performs DESCAM (Decompose, Enumerate, Scanning, Catalog, Analysis, Merge) review to software for Open Source License Compliance.

The tool can extract (Decompose) archive files like Jar, ZIP, Tarballs, RPM, Debian, etc., to recursively obtain the list of assets (Enumerate) contained.

XMonkey Curator also performs a basic review (Scanning) of the assets to extract information as "features" for OSLC assessments.
Scan types supported:
- Literal Strings
- Regex Patterns (*example*).
- Symbols Matching using predefined *signatures*.

The results of the review can be automatically processed (Catalog) using predefined *rules* and workflows (Analysis).

## Usage

```
$ pip install xmonkey-curator
$ xmonkey-curator [OPTIONS] PATH
```
