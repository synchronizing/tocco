from tocco.utils import classproperty, humansize, runcommand

import psutil
import time


class battery(object):
    battery = psutil.sensors_battery()

    @classproperty
    def percent(cls):
        return "{}%".format(cls.battery.percent)

    @classproperty
    def hours_left(cls):
        plugged = cls.battery.power_plugged
        secsleft = cls.battery.secsleft

        if type(secsleft) == int and not plugged:
            if secsleft == 0:
                return "Loading"
            else:
                mm, ss = divmod(cls.battery.secsleft, 60)
                hh, mm = divmod(mm, 60)
                hours_left = "%d:%02d" % (hh, mm)
                return "{}h".format(hours_left)
        elif plugged:
            return "Plugged"
        else:
            return "Loading"


class disk(object):
    usage = psutil.disk_usage("/")

    @classproperty
    def total(cls):
        return humansize(cls.usage.total)

    @classproperty
    def used(cls):
        return humansize(cls.usage.used)

    @classproperty
    def free(cls):
        return humansize(cls.usage.free)

    @classproperty
    def percent(cls):
        return "{}%".format(cls.usage.percent)


class memory(object):
    memory = psutil.virtual_memory()

    @classproperty
    def total(cls):
        return humansize(cls.memory.total)

    @classproperty
    def available(cls):
        return humansize(cls.memory.available)

    @classproperty
    def used(cls):
        return humansize(cls.memory.used)

    @classproperty
    def free(cls):
        return humansize(cls.memory.free)

    @classproperty
    def active(cls):
        return humansize(cls.memory.active)

    @classproperty
    def inactive(cls):
        return humansize(cls.memory.inactive)

    @classproperty
    def wired(cls):
        return humansize(cls.memory.wired)

    @classproperty
    def percent(cls):
        return "{0:.2f}%".format(100.0 - cls.memory.percent)


class network(object):
    before = psutil.net_io_counters(pernic=False)

    @classproperty
    def sent_last_sec(cls):
        network_before = psutil.net_io_counters(pernic=False)
        time.sleep(1)
        network_after = psutil.net_io_counters(pernic=False)

        return humansize(network_after.bytes_sent - network_before.bytes_sent)

    @classproperty
    def received_last_sec(cls):
        network_before = psutil.net_io_counters(pernic=False)
        time.sleep(1)
        network_after = psutil.net_io_counters(pernic=False)

        return humansize(network_after.bytes_recv - network_before.bytes_recv)


class cpu(object):
    @classproperty
    def percent(cls):
        return "{}%".format(psutil.cpu_percent(interval=1))

    class temperature(object):
        base = (
            next(
                runcommand(
                    "/usr/local/bin/istats cpu temp --no-scale --no-graphs --no-labels".split()
                )
            )
            .split()[0]
            .decode("latin-1")
        )

        @classproperty
        def C(cls):
            return "{0:.2f} °C".format(float(cls.base))

        @classproperty
        def F(cls):
            return "{0:.2f} °F".format(float(cls.base) * (9 / 5) + 32)
