#!/bin/bash
rm -rf dist/*
python3 setup.py sdist bdist_wheel > scripts/build.log
pip3 install dist/xmonkey_curator-*-py3-none-any.whl --force-reinstall > scripts/install.log
echo '' > scan_report.json
echo '' > debug.log