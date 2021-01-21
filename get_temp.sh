#!/bin/sh
source ./temper_env.rc

EXTRA_BAD_TEMP_ARGS=
EXTRA_GET_TEMP_ARGS=

usage(){
    cat <<END

Usage:
--silent-if-ok: doesn't show a correct device message.
-f: display the temperature in fahrenheit

END
}

ANY_ARGS=false

for var in "$@"
do
    if [ "@$var" = "@--silent-if-ok" ]; then
        EXTRA_BAD_TEMP_ARGS="$EXTRA_BAD_TEMP_ARGS --silent-if-ok"
    elif [ "@$var" = "@-f" ]; then
        EXTRA_GET_TEMP_ARGS="$EXTRA_BAD_TEMP_ARGS -f"
    else
        echo "unknown argument: $var"
        usage
        exit 1
    fi
    ANY_ARGS=true
done

if [ "@$ANY_ARGS" = "@false" ]; then
    usage
fi

if [ ! -f "`command -v virtualenv`" ]; then
    INSTALL_CMD=dnf install -y
    $INSTALL_CMD python3-virtualenv
fi

if [ -d "$THIS_VENV" ]; then
    source $ACTIVATOR
    python -c "import temperusb"
    if [ $? -ne 0 ]; then
        cat << END
The dependencies are broken in $THIS_VENV (probably from upgrading to a
new a major revision of your distro), so it will be DELETED and remade.
END
        rm -Rf "$THIS_VENV"
    fi
fi

if [ ! -d "$THIS_VENV" ]; then
    python -m virtualenv "$THIS_VENV"
fi

source $ACTIVATOR
if [ $? -ne 0 ]; then
    echo
    echo "Error:"
    echo "Activating the virtual environment using $ACTIVATOR failed."
    echo
    exit 4
fi

python -c "import temperusb"
if [ $? -ne 0 ]; then
    echo "* installing temperusb..."
    python -m pip install --upgrade pip
    python -m pip install --upgrade setuptools wheel
    python -m pip install --upgrade temperusb
fi
python -c "import temper"
TEMPER_CODE=$?
THIS_TEMPER=https://github.com/ccwienk/temper/archive/master.zip
# ^ This fork of https://github.com/urwen/temper/network
# is maintained better and has a setup.py.
if [ $TEMPER_CODE -ne 0 ]; then
    echo "* installing $THIS_TEMPER..."
    python -m pip install --upgrade $THIS_TEMPER
    python -c "import temper"
    TEMPER_CODE=$?
fi
python bad_temper.py $EXTRA_BAD_TEMP_ARGS
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
as python cannot import temperusb.
END
    exit 4
fi

python -c "import temper"
# ^ https://github.com/urwen/temper

if [ $? -ne 0 ]; then
    cat << END
The script $0 is unable to create/repair the venv: $THIS_VENV
as python cannot import temper.
END
    exit 4
fi
# python TemperatureSanitizer.py
python get_temp.py $EXTRA_GET_TEMP_ARGS
TEMP_RESULT=$?
if [ $TEMP_RESULT -ne 0 ]; then
    exit $TEMP_RESULT
fi
