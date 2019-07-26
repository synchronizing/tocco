import subprocess


class classproperty(object):
    """ Creates a decorator that is basically @staticmethod + @property.

    Note:
        This allows us to essentially call methods without initializing a
        class, or call the method as a function.

    Example:
        class Example():
            @classproperty
            def current_time(cls):
                return time.now()

        We can then call the above function simply as "example.current_time".
    """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def humansize(nbytes):
    """ Appends prefix to bytes for human readability. """

    suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


def runcommand(command):
    """ Runs commands via bash, and returns the print out of command. """

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b"")
