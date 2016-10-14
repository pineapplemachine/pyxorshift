import numpy
import calendar
from datetime import datetime

class xorshift(object):
    def __init__(self, *args):
        self.seed(*args)
    def seed(self, *args):
        if len(args) > 4:
            raise ValueError('Algorithm accepts at maximum 4 integral seeds.')
        self.x = numpy.uint64(args[0] if len(args) > 0 else 0x123436789abcdef0)
        self.y = numpy.uint64(args[1] if len(args) > 1 else 0x456123abcdef0123)
        self.z = numpy.uint64(args[2] if len(args) > 2 else 0x9576503210fedcba)
        self.w = numpy.uint64(args[3] if len(args) > 3 else 0x6666666666666666)
    def next(self):
        t = self.x
        t ^= numpy.left_shift(t, numpy.uint64(11))
        t ^= numpy.right_shift(t, numpy.uint64(8))
        self.x = self.y
        self.y = self.z
        self.z = self.w
        self.w ^= numpy.right_shift(self.w, numpy.uint64(19))
        self.w ^= t
        return int(self.w)
    def rand_int(self, min, max):
        """
        Get a random integral from min (inclusive) to max (exclusive).
        """
        if min == max:
            return min
        else:
            return int(min + (self.next() % (max - min)))
    def rand_float(self, min = 0, max = 1):
        """
        Get a random floating point number from min (inclusive) to max (inclusive).
        """
        return float(min + (self.next() / float(18446744073709551615) * (max - min)))
    def rand_bool(self):
        """
        Get a random boolean value.
        """
        return True if self.rand_int(0, 2) else False
    def rand_datetime(self, min = 1, max = 2147483647):
        """
        Get a random datetime between a min and max timestamp.
        Timestamps may be datetime objects, or numbers representing epoch time.
        """
        if isinstance(min, datetime):
            min = calendar.timegm(min.timetuple())
        if isinstance(max, datetime):
            max = calendar.timegm(max.timetuple())
        return datetime.utcfromtimestamp(self.rand_int(min, max))
    def rand_string(self, min_length, max_length, allowed_chars):
        """
        Build a string of random length within the given bounds and using
        the given characters.
        """
        length = self.rand_int(
            min_length, max_length if max_length is not None else min_length
        )
        return ''.join((
            self.rand_from(*allowed_chars) for i in range(0, length)
        ))
    def rand_alpha_string(self, min_length, max_length=None):
        """
        Build a string of random length within the given bounds with
        upper- and lower-case English letters.
        """
        return self.rand_string(min_length, max_length,
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        )
    def rand_numeric_string(self, min_length, max_length=None):
        """
        Build a string of random length within the given bounds with
        numeric digits.
        """
        return self.rand_string(min_length, max_length,
            '0123456789'
        )
    def rand_alphanumeric_string(self, min_length, max_length=None):
        """
        Build a string of random length within the given bounds with
        numeric digits and upper- and lower-case English letters.
        """
        return self.rand_string(min_length, max_length,
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )
    def rand_from(self, *args):
        """
        Return a random argument from the passed arguments.
        """
        if not args:
            raise ValueError('Must pass at least one choice argument.')
        return args[self.rand_int(0, len(args))]
    def rand_list(self, min_length, max_length, make_item):
        length = self.rand_int(
            min_length, max_length if max_length is not None else min_length
        )
        items = []
        for i in range(0, length):
            items.append(make_item())
        return items
