# -*- coding: UTF-8 -*-

import base64
import hashlib

from django.utils import importlib
from django.utils.crypto import (
    pbkdf2, constant_time_compare, get_random_string)
from django.utils.datastructures import SortedDict


def mask_hash(hash, show=6, char="*"):
    """
    Returns the given hash, with only the first ``show`` number shown. The
    rest are masked with ``char`` for security reasons.
    """
    masked = hash[:show]
    masked += char * len(hash[show:])
    return masked


class BasePasswordHasher(object):
    """
    Abstract base class for password hashers

    When creating your own hasher, you need to override algorithm,
    verify(), encode() and safe_summary().

    PasswordHasher objects are immutable.
    """
    algorithm = None
    library = None

    def _load_library(self):
        if self.library is not None:
            if isinstance(self.library, (tuple, list)):
                name, mod_path = self.library
            else:
                name = mod_path = self.library
            try:
                module = importlib.import_module(mod_path)
            except ImportError:
                raise ValueError("Couldn't load %s password algorithm "
                                 "library" % name)
            return module
        raise ValueError("Hasher '%s' doesn't specify a library attribute" %
                         self.__class__)

    def salt(self):
        """
        Generates a cryptographically secure nonce salt in ascii
        """
        return get_random_string()

    def verify(self, password, encoded):
        """
        Checks if the given password is correct
        """
        raise NotImplementedError()

    def encode(self, password, salt):
        """
        Creates an encoded database value

        The result is normally formatted as "algorithm$salt$hash" and
        must be fewer than 128 characters.
        """
        raise NotImplementedError()

    def safe_summary(self, encoded):
        """
        Returns a summary of safe values

        The result is a dictionary and will be used where the password field
        must be displayed to construct a safe representation of the password.
        """
        raise NotImplementedError()


class PBKDF2PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the PBKDF2 algorithm (recommended)

    Configured to use PBKDF2 + HMAC + SHA256 with 10000 iterations.
    The result is a 64 byte binary string.  Iterations may be changed
    safely but you must rename the algorithm if you change SHA256.
    """
    algorithm = "pbkdf2_sha256"
    iterations = 10000
    digest = hashlib.sha256

    def encode(self, password, salt, iterations=None):
        assert password
        assert salt and '$' not in salt
        if not iterations:
            iterations = self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def verify(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt, int(iterations))
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return SortedDict([
            (('algorithm'), algorithm),
            (('iterations'), iterations),
            (('salt'), mask_hash(salt)),
            (('hash'), mask_hash(hash)),
        ])
