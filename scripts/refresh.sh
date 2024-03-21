#!/bin/bash
python3 setup.py sdist bdist_wheel > scripts/build.log
pip install dist/xmonkey_curator-0.1.0-py3-none-any.whl --force-reinstall > scripts/install.log
echo '' > scan_report.json