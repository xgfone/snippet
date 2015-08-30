#!/bin/bash
#
# Install the vimrc
#    https://github.com/xgfone/dot-vimrc
#

## Install Dependencie
yaourt -S ack ctags &> /dev/null                            # ArchLinux
sudo apt-get install ack-grep exuberant-ctags &> /dev/null  # Ubuntu
brew install ack ctags  &> /dev/null                        # OS X

# Backup your old vim configuration files
mv ~/.vim ~/.vim.orig  &> /dev/null
mv ~/.vimrc ~/.vimrc.orig  &> /dev/null

# Clone and install this repo
git clone git://github.com/xgfone/dot-vimrc.git ~/.vim
ln -s ~/.vim/vimrc ~/.vimrc

# Setup Vundle
git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle

# Last, you can execute the vim, and install bundles.
# :BundleInstall
