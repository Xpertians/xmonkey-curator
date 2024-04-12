#!/bin/bash
rm -rf dist/* build/*
#pip3 uninstall xmonkey-curator -y
#rm -rf /opt/homebrew/lib/python3.12/site-packages/xmonkey_curator/
python3 setup.py sdist bdist_wheel > scripts/build.log
pip3 install dist/xmonkey_curator-*-py3-none-any.whl --force-reinstall > scripts/install.log
echo '' > scan_report.json
echo '' > debug.log