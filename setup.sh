#!/bin/bash

# 1. Installs iStats
sudo gem install iStats

# 2. Installs or updates.
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# 3. Installs Python3.
brew install python3

# 4. Installs Tocco
/usr/local/bin/python3 -m pip install git+http://github.com/synchronizing/Tocco
