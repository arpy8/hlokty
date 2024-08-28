#!/bin/bash

ensure_in_path() {
    if [[ ":$PATH:" != *":$1:"* ]]; then
        export PATH="$1:$PATH"
    fi
}

if ! command -v python3 &> /dev/null
then
    brew install python
fi

if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

PYTHON_BIN_DIR="$(python3 -m site --user-base)/bin"
ensure_in_path "$PYTHON_BIN_DIR"

pip3 install -q https://files.pythonhosted.org/packages/9c/c7/28adb2d48dedf9e10212e6b5e1dabe4801319664e6152179dd53748a8fe6/hlokty-0.1.tar.gz && hlokty -s
