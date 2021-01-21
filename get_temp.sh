#!/bin/sh
if [ ! -d ~/venv ]; then
    mkdir -p ~/venv
fi
THIS_VENV=~/venv/temperusb

if [ ! -f "`command -v virtualenv`" ]; then
    INSTALL_CMD=dnf install -y
    $INSTALL_CMD python3-virtualenv
fi

if [ -d "$THIS_VENV" ]; then
    source $THIS_VENV/bin/activate
    python3 -c "import temperusb"
    if [ $? -ne 0 ]; then
        cat << END
The dependencies are broken in $THIS_VENV (probably from upgrading to a
new a major revision of your distro), so it will be DELETED and remade.
END
        rm -Rf "$THIS_VENV"
    fi
fi

if [ ! -d "$THIS_VENV" ]; then
    python3 -m virtualenv "$THIS_VENV"
fi

source $THIS_VENV/bin/activate
python -c "import temperusb"
if [ $? -ne 0 ]; then
    echo "* installing temperusb..."
    python -m pip install --upgrade pip
    python -m pip install --upgrade setuptools wheel
    python -m pip install --upgrade temperusb
fi
python3 -c "import temper"
TEMPER_CODE=$?
THIS_TEMPER=https://github.com/ccwienk/temper/archive/master.zip
# ^ This fork of https://github.com/urwen/temper/network
# is maintained better and has a setup.py.
if [ $TEMPER_CODE -ne 0 ]; then
    echo "* installing $THIS_TEMPER..."
    python -m pip install --upgrade $THIS_TEMPER
    python3 -c "import temper"
    TEMPER_CODE=$?
fi
python bad_temper.py
if [ $? -eq 2 ]; then
    # python -m pip install --upgrade pip
    # python -m pip install --upgrade setuptools wheel
    python -m pip uninstall -y temper
    # ^ This is NOT a usb sensor tool!
fi

python -c "import temperusb"
# ^ doesn't support 413d:2107
# such as https://www.amazon.com/gp/product/B009YRP906/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1
if [ $? -ne 0 ]; then
    cat << END
The script $0 is unable to create/repair the venv: $THIS_VENV
as the dependency still will not import.
END
    exit 1
fi
python -c "import temper"
# ^ https://github.com/urwen/temper

if [ $? -ne 0 ]; then
    cat << END
The script $0 is unable to create/repair the venv: $THIS_VENV
as the dependency still will not import.
END
    exit 1
fi
# python TemperatureSanitizer.py
python TemperatureSanitizer_413d_2107.py
