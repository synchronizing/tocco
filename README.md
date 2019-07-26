# 👆🏼Tocco
### Italian for Touch

This is a collection of useful Python commands that was created to be utilized with `Simple`, an upcoming [`BetterTouchTool`](https://folivora.ai/) snippet being created for simplicity, and intuition. While `Simple` has not yet been published, `Tocco` has been made open-source if other developers would wish to use it.

## Installing

For `Tocco` to work you must first install some dependencies. You may either do so manually by following the instructions below, or by running the `setup_tocco.sh` file within the root directory of this project.

1. Install iStats via gem, `sudo gem install iStats`
2. Install Brew via [brew.sh](https://brew.sh)
3. Install Python3 via brew, `brew install python3`
4. Install Tocco via Python3, `/usr/local/bin/python3 -m pip install git+http://github.com/synchronizing/Tocco`
5. Install `Simple` (coming soon!)

## Using `Tocco`

`Tocco` was made to be as easy as possible to be used:

```python
import tocco

# Battery
print(tocco.battery.percent)
print(tocco.battery.hours_left)

# CPU
print(tocco.cpu.percent)
print(tocco.cpu.temperature.C)
print(tocco.cpu.temperature.F)

# Disk
print(tocco.disk.total)
print(tocco.disk.used)
print(tocco.disk.free)
print(tocco.disk.percent)

# Memory
print(tocco.memory.total)
print(tocco.memory.available)
print(tocco.memory.used)
print(tocco.memory.free)
print(tocco.memory.active)
print(tocco.memory.inactive)
print(tocco.memory.wired)
print(tocco.memory.percent)

# Network
print(tocco.network.sent_last_sec)
print(tocco.network.received_last_sec)
```

To display any of the above information on your `BetterTouchTool` preset, simply add a "Shell Script/Task Widget" and then paste the following in (using `tocco.battery.hours.left` as example):

```bash
/usr/local/bin/python3 -c "import tocco; print(tocco.battery.hours_left)"
```

Setting the refresh of the script allows easy management of the information that will display to the end user.
