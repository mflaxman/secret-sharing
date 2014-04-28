# -*- coding: utf-8 -*-
"""
    Secret Sharing
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import string
from characters import charset_to_int, int_to_charset

from .utils import (get_large_enough_prime, random_polynomial,
                    get_polynomial_points, modular_lagrange_interpolation)


class Secret():
    def __init__(self, secret_int):
        if not isinstance(secret_int, (int, long)) and secret_int >= 0:
            raise ValueError("Secret must be a non-negative integer.")
        self._secret = secret_int

    @staticmethod
    def share_to_point(share):
        '''
        share should be in the format:
          `1-2130008653...` for int
        '''
        x, y = share.split('-')
        return int(x), int(y)

    @staticmethod
    def point_to_share(point):
        '''
        point should be in the format (1, 4938573982723...)
        '''
        if isinstance(point, tuple) and len(point) == 2:
            if isinstance(point[0], (int, long)):
                if isinstance(point[1], (int, long)):
                    x, y = point
                    if x > 255:
                        msg = 'The largest x coordinate for a share is 255.'
                        raise ValueError(msg)

                    return '%s-%s' % (x, y)

        raise ValueError('Point format is invalid. Must be integer pair.')

    @classmethod
    def from_charset(cls, secret, charset):
        if not isinstance(secret, str):
            raise ValueError("Secret must be a string.")
        if not isinstance(charset, str):
            raise ValueError("Charset must be a string.")
        if (set(secret) - set(charset)):
            msg = "Secret contains characters that aren't in the charset."
            raise ValueError(msg)
        secret_int = charset_to_int(secret, charset)
        return cls(secret_int)

    @classmethod
    def from_shares(cls, shares):
        if not isinstance(shares, list):
            raise ValueError("Shares must be in list form.")
        for share in shares:
            if not isinstance(share, str):
                raise ValueError("Each share must be a string.")
        points = []
        for share in shares:
            # HIDEOUS HACK
            # This allows us to call the correct share_to_point method if
            # this class hass been inhereted
            class_to_use = cls(1)
            points.append(class_to_use.share_to_point(share))
        x_values, y_values = zip(*points)
        prime = get_large_enough_prime(y_values)
        secret_int = modular_lagrange_interpolation(0, points, prime)
        return cls(secret_int)

    def split(self, threshold, num_shares):
        '''
        Split the secret into shares.
        The threshold is the total # of shares required to recover the secret.

        Default is int
        Feel free to add your own.
        '''
        if threshold < 2:
            raise ValueError("Threshold must be >= 2.")
        if threshold > num_shares:
            raise ValueError("Threshold must be < the total number of shares.")
        prime = get_large_enough_prime([self._secret, num_shares])
        if not prime:
            msg = "Error! Secret is too long for share calculation!"
            raise ValueError(msg)
        coefficients = random_polynomial(threshold-1, self._secret, prime)
        points = get_polynomial_points(coefficients, num_shares, prime)
        shares = []
        for point in points:
            shares.append(self.point_to_share(point))
        return shares

    @classmethod
    def from_printable_ascii(cls, secret):
        return cls.from_charset(secret, string.printable)

    def as_int(self):
        return self._secret

    def as_charset(self, charset):
        return int_to_charset(self.as_int(), charset)

    def as_printable_ascii(self):
        return self.as_charset(string.printable)
