#!/bin/bash

# ENV:
#  1. Add or modify the software source.
#  2. If Debian/Ubuntu, update the software cache:
#      sudo apt-get update

SUDO=sudo
CMD="apt-get"
OPT="-y"

# Base
SOFTWARES="vim git subversion"

# Developer
SOFTWARES="$SOFTWARES build-essential gcc g++ make"

# Install other softwares
# vinagre is a remote desktop client(SSH, VNC, RDP)
SOFTWARES="$SOFTWARES vim-gtk openfetion thunderbird wireshark vinagre"
#SOFTWARES="$SOFTWARES chromium"
SOFTWARES="$SOFTWARES chmsee filezilla"
#SOFTWARES="$SOFTWARES terminator"
SOFTWARES="$SOFTWARES virtualbox"

# Sound and Video
SOFTWARES="$SOFTWARES vlc audacious"
#SOFTWARES="$SOFTWARES flashplugin-installer"

# System
SOFTWARES="$SOFTWARES gparted gpart"


# Usage
function usage()
{
    prog=$(basename $1)
    echo
    echo "Usage:"
    echo "    $prog [--cmd CMD] [--opt OPTS] [--confvim] [--confonly] [SOFTWARE ...]"
    echo
    echo "Args:"
    echo "    --cmd CMD"
    echo "         apt-get, aptitude for DEB, or yum ofr RPM, default apt-get"
    echo "    --opt OPTS"
    echo '         the options of CMD, default "y"'
    echo "    --confvim"
    echo "         install the vim default; and if has the option, will config vim"
    echo "    --confonly"
    echo "         Only config the softwares"
    echo "    SOFTWARE ..."
    echo "         extra softwares except default"
    echo
}

# Install
function install_software()
{
    $SUDO $CMD $OPT install $SOFTWARES
}

# Configure the vim
function config_vim()
{
    mv ~/.vim ~/.vim.orig 2&>1
    mv ~/.vimrc ~/.vimrc.orig 2&>1
    git clone https://github.com/xgfone/dot-vimrc.git ~/.vim
    git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
    ln -s ~/.vim/vimrc ~/.vimrc
}

EXTRA_SOFTWARES=
CONFIG_VIM="n"
CONFIG_ONLY="n"
while :
do
    case $1 in
        --help)
            usage $0; exit 1;;
        --cmd)
            if [ -z "$2" ]; then
                echo 'Option `--cmd` requires a argument.'; usage $0; exit 1;
            else
                CMD="$2"; shift 2;
            fi
            ;;
        --opt)
            if [ -z "$2" ]; then
                echo 'Option `--opt` requires a argument.'; usage $0; exit 1;
            else
                OPT="$2"; shift 2;
            fi
            ;;
        --confvim)
            CONFIG_VIM="y"; shift;;
        --confonly)
            CONFIG_ONLY="y"; shift;;
        --)
            shift; break;;
        -*)
            echo "Invalid argument: $1"; usage $0; exit 1;;
        [a-zA-Z0-9]*)
            if [ -n "$1" ]; then
                EXTRA_SOFTWARES="$EXTRA_SOFTWARES $1"; shift;
            else
                break;
            fi
            ;;
        *)
            break;;
    esac
done

if [ "$CONFIG_ONLY" == "y" ]; then
    echo "Configure ......"
    config_vim
    exit 0
fi

SOFTWARES="$SOFTWARES $EXTRA_SOFTWARES"
echo "Will execute the following command to install"
echo
echo $CMD $OPT install $SOFTWARES
echo
echo -n 'Please input `y` to install, or `n` not?  '
read yes
if [ -n "$yes" ] && [ "$yes" == "y" ] || [ "$yes" == "yes" ]; then
    echo "Starting to install ..."
    install_software
    if [ "$CONFIG_VIM" == "y" ]; then
        echo "Starting to configure vim ..."
        config_vim
    fi
    echo
    echo "Install successfully!"
elif [ "$yes" == "n" ] || [ "$yes" == "not" ]; then
    echo "Exiting ..."
else
    echo "Input ERROR! "
fi
echo


# Subsequent operate
#   1. Open the vim, and execute the `BundleInstall` command to install the vim plugins.
#   2. Install the wps office.
#   3. If `flashplugin-installer` is not installed, need to install the adobe flash player by hand.
#   4. Install and configure the Golang.
#   5. Install and configure the sublimetext.
#   6. (Optional) Install and configure the eclipse.
