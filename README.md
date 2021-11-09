# 👆🏼 tocco
### Italian for Touch

A tool for easily getting information about the current computer. Intended for use with [`BetterTouchTool`](https://folivora.ai/). 

## Installing

```
/bin/bash -c "$(curl -fsSL https://github.com/synchronizing/tocco/blob/master/setup.sh)"
```

## Using

```python
import tocco

# Battery
print(tocco.battery.percent)
print(tocco.battery.hours_left)

# CPU
print(tocco.cpu.percent)
print(tocco.cpu.temperature.C)
print(tocco.cpu.temperature.F)

# GPU
print(tocco.gpu.temperature.C)
print(tocco.gpu.temperature.F)

# Fan
print(tocco.fans.rpm)

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

To display any of the above information on your `BetterTouchTool` preset, simply add a "Shell Script/Task Widget" and then paste the following in (using `tocco.battery.hours_left` as example):

```bash
/usr/local/bin/python3 -c "import tocco; print(tocco.battery.hours_left)"
```

Setting the refresh of the script allows easy management of the information that will display to the end user.
