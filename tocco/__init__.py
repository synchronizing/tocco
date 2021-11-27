import subprocess
import time

import psutil
from toolbox.builtins.property import classproperty


def humansize(nbytes):
    """Appends prefix to bytes for human readability."""

    suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


def runcommand(command):
    """Runs commands via bash, and returns the print out of command."""

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b"")


class battery(object):
    """Information about the systems battery."""

    battery = psutil.sensors_battery()

    @classproperty
    def percent(cls):
        """Retrieves and formats the systems battery percentage.

        Returns:
            str: Battery percentage of the system.
        """
        return "{}%".format(cls.battery.percent)

    @classproperty
    def hours_left(cls):
        """Retrieves and formarts the charge left in the battery.

        Returns:
            str: How much time is left on the battery charge. Returns "Plugged"
            if the computer is plugged, or "Loading" if the system is still calculating
            how much charge is still left.
        """
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
    """Information about the systems drive."""

    usage = psutil.disk_usage("/")

    @classproperty
    def total(cls):
        """Total disk space.

        Returns:
            str: How much space is left with proper byte classification (b, kb, mb, etc.)
        """
        return humansize(cls.usage.total)

    @classproperty
    def used(cls):
        """Disk space that is already used.

        Returns:
            str: How much space has been used with proper byte classification (b, kb, mb, etc.)
        """
        return humansize(cls.usage.used)

    @classproperty
    def free(cls):
        """Disk space is that currently free.

        Returns:
            str: How much space is free with proper byte classification (b, kb, mb, etc.)
        """
        return humansize(cls.usage.free)

    @classproperty
    def percent(cls):
        """Percentage of the disk space that is free.

        Returns:
            str: Percentage of disk that is free.
        """
        return "{}%".format(cls.usage.percent)


class memory(object):
    """Information about the disks memory."""

    memory = psutil.virtual_memory()

    @classproperty
    def total(cls):
        """Total physical memory in the system.

        Returns:
            str: Total memory space with proper byte classification (b, kb, mb, etc.)
        """
        return humansize(cls.memory.total)

    @classproperty
    def available(cls):
        """Memory that can be given instantly to processes without the system
        going into swap.

        Note:
            This is calculated by summing different memory values depending on
            the platform and it is supposed to be used to monitor actual memory
            usage in a cross platform fashion.

        Returns:
            str: Available memory space with proper byte classification (b, kb, mb, etc.)
        """
        return humansize(cls.memory.available)

    @classproperty
    def used(cls):
        """Memory used, calculated differently depending on the platform and
        designed for informational purposes only.

        Note:
            total - free does not necessarily match used.

        Returns:
            (str): Used memory space with proper byte classification (b, kb, mb, etc.)
        """
        return humansize(cls.memory.used)

    @classproperty
    def free(cls):
        """Memory not being used at all (zeroed) that is readily available;

        Note:
            total - used does not necessarily match free.

        Returns:
            (str): Free memory space with proper byte classification (b, kb, mb, etc.)
        """
        return humansize(cls.memory.free)

    @classproperty
    def active(cls):
        """Memory currently in use or very recently used, and so it is in RAM.

        Returns:
            str: Active memory space with proper byte classification (b, kb, mb, etc.)
        """
        return humansize(cls.memory.active)

    @classproperty
    def inactive(cls):
        """Memory that is marked as not used.

        Returns:
            str: Memory that is marked as not used with proper byte classification (b, kb, mb, etc.)
        """

        return humansize(cls.memory.inactive)

    @classproperty
    def wired(cls):
        """Memory that is marked to always stay in RAM. It is never moved to disk.

        Returns:
            str: Memory that sticks to RAM with proper byte classification (b, kb, mb, etc.)
        """
        return humansize(cls.memory.wired)

    @classproperty
    def percent(cls):
        """Percent of memory that is currently available to the user.

        Returns:
            str: Percent to two decimals of currently available memory.
        """
        return "{0:.2f}%".format(100.0 - cls.memory.percent)


class network(object):
    """Information about the network."""

    before = psutil.net_io_counters(pernic=False)

    @classproperty
    def sent_last_sec(cls):
        """Measurement of bytes sent in the last second of function execution.

        Returns:
            str: Bytes transferred in the last second with proper classification (b, kb, mb, etc.)
        """
        network_before = psutil.net_io_counters(pernic=False)
        time.sleep(1)
        network_after = psutil.net_io_counters(pernic=False)

        return humansize(network_after.bytes_sent - network_before.bytes_sent)

    @classproperty
    def received_last_sec(cls):
        """Measurement of bytes received in the last second of function execution.

        Returns:
            str: Bytes received in the last second with proper classification (b, kb, mb, etc.)
        """
        network_before = psutil.net_io_counters(pernic=False)
        time.sleep(1)
        network_after = psutil.net_io_counters(pernic=False)

        return humansize(network_after.bytes_recv - network_before.bytes_recv)


class cpu(object):
    """Information about the CPU."""

    @classproperty
    def percent(cls):
        """Percentage of the CPU being used.

        Returns:
            str: Percentage of CPU being used with proper % formatting.
        """
        return "{}%".format(psutil.cpu_percent(interval=1))

    class temperature(object):
        """Temperature class of the CPU.

        Note:
            This classes uses iStat until a complete Python or native system
            replacement is able to be figured out.
        """

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
            """Temperature of CPU in celcius.

            Returns:
                str: Temperature of CPU in celcius and to two decimal places.
            """
            return "{0:.2f} °C".format(float(cls.base))

        @classproperty
        def F(cls):
            """Temperature of CPU in fahrenheit.

            Returns:
                str: Temperature of CPU in fahrenheit and to two decimal places.
            """
            return "{0:.2f} °F".format(float(cls.base) * (9 / 5) + 32)


class gpu(object):
    """Information about the GPU."""

    class temperature(object):
        """Temperature class of the GPU.

        Note:
            This classes uses iStat until a complete Python or native system
            replacement is able to be figured out.
        """

        base = (
            next(runcommand("/usr/local/bin/istats scan Th1H --no-labels".split()))
            .split()[0]
            .decode("latin-1")
        )

        @classproperty
        def C(cls):
            """Temperature of CPU in celcius.

            Returns:
                str: Temperature of CPU in celcius and to two decimal places.
            """
            return "{0:.2f} °C".format(float(cls.base))

        @classproperty
        def F(cls):
            """Temperature of CPU in fahrenheit.

            Returns:
                str: Temperature of CPU in fahrenheit and to two decimal places.
            """
            return "{0:.2f} °F".format(float(cls.base) * (9 / 5) + 32)


class fans(object):
    """Information about the fans."""

    base = (
        next(runcommand("/usr/local/bin/istats fan speed --value-only".split()))
        .split()[0]
        .decode("latin-1")
    )

    @classproperty
    def rpm(cls):
        """Rotation per minute of the fans.

        Returns:
            str: RPM of the fans.
        """
        return "{} RPM".format(cls.base)
