import multiprocessing


class SharedValue:
    _manager = multiprocessing.Manager()  # shared manager for strings

    def __init__(self, typecode="i", initial=0):
        if typecode == "s":  # string
            self._type = "s"
            self._value = SharedValue._manager.Value(str, str(initial))
        elif typecode == "d":  # float
            self._type = "d"
            self._value = multiprocessing.Value("d", float(initial))
        elif typecode == "i":  # int
            self._type = "i"
            self._value = multiprocessing.Value("i", int(initial))
        else:
            raise ValueError("Unsupported typecode. Use 'i', 'd', or 's'.")

    def get(self):
        return self._value.value

    def set(self, val):
        self._value.value = val

    def inc(self, delta=1):
        if self._type in ("i", "d"):
            with self._value.get_lock():
                self._value.value += delta
        else:
            raise TypeError("Cannot increment non-numeric SharedValue.")

    def dec(self, delta=1):
        self.inc(-delta)

    def __str__(self):
        return str(self.get())

    def __repr__(self):
        return f"SharedValue({self.get()!r})"

    def __int__(self):
        return int(self.get())

    def __float__(self):
        return float(self.get())

    def __eq__(self, other):
        return self.get() == other

    def __lt__(self, other):
        return self.get() < other

    def __le__(self, other):
        return self.get() <= other
