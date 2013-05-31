#!/usr/bin/env python3


import re


"""This is main module for semver.py - Semantic Versioning
library for Python3 language.
"""


__version__ = '0.1.3'


valid_identifier_regexp = re.compile('^[0-9A-Za-z-]*$')
base_regexp = ('[0-9]+\.[0-9]+\.[0-9]+'                     # major.minor.patch
               '(-([0-9A-Za-z-]+)(\.[0-9A-Za-z-]+)*)?'      # prerelease
               '(\+([0-9A-Za-z-]+)(\.[0-9A-Za-z-]+)*)?')    # build
match_regexp = re.compile('^{0}$'.format(base_regexp))


class InvalidVersionStringError(Exception):
    pass


class InvalidIdentifierError(Exception):
    pass


def _prerelzip(a, b):
    """Zips two prerelease lists.
    If one is longer it will not truncate but
    fill with integer `-1`.
    """
    n = max(len(a), len(b))
    zipped = []
    for i in range(n):
        try: m = a[i]
        except IndexError: m = -1
        finally: pass
        try: n = b[i]
        except IndexError: n = -1
        finally: pass
        zipped.append((m, n))
    return zipped


def _split(string):
    """Splits version string into main version,
    prerelease and build metadata.
    """
    version, prerelease, build = '', '', ''
    if '-' in string:
        n = string.index('-')
        version = string[:n]
        prerelease = string[n+1:]
    else:
        version = string

    if '+' in prerelease:
        n = prerelease.rindex('+')
        build = prerelease[n+1:]
        prerelease = prerelease[:n]
    if '+' in version:
        n = version.rindex('+')
        build = version[n+1:]
        version = version[:n]
    return (version, prerelease, build)


def valid(string):
    """Returns True if given string is
    a valid version string.
    """
    return match_regexp.match(string) is not None


class Comparison():
    """Class utilizing version comparison functionality.

    First version is always compared to the second which means that
    `lt()` assumes: `first < second`.

    Also remember that integers are *greater* than strings so
        0 > 'a' -> True
        0 < 'a' -> False
    """
    def __init__(self, first, second):
        """:param first: first version
        :type first: str
        :param second: second version
        :type second: str
        """
        self.first = first
        self.second = second

    def _prereleasegt(self, n):
        """Checks if prerelease identifiers of first are greater than second.

        :param n: index at which we are starting comparison
        :type n: int
        """
        result = False
        first, second = _prerelzip(self.first.prerelease[n:], self.second.prerelease[n:])[0]
        try:
            comp = first > second
        except TypeError:
            if type(first) == int: comp = True
            else: comp = False
        finally:
            if comp or self._prereleasegt(n=n+1): result = True
        return result

    def _prereleaselt(self, n):
        """Checks if prerelease identifiers of first are lesser than second.

        :param n: index at which we are starting comparison
        :type n: int
        """
        result = False
        first, second = _prerelzip(self.first.prerelease[n:], self.second.prerelease[n:])[0]
        try:
            comp = first < second
        except TypeError:
            if type(first) == int: comp = False
            else: comp = True
        finally:
            if comp or self._prereleaselt(n=n+1): result = True
        return result

    def eq(self):
        result = False
        major = self.first.major == self.second.major
        minor = self.first.minor == self.second.minor
        patch = self.first.patch == self.second.patch
        prerelease = self.first.prerelease == self.second.prerelease
        result = major and minor and patch and prerelease
        return result

    def gt(self):
        result = False
        eqmajor = self.first.major == self.second.major
        eqminor = self.first.minor == self.second.minor
        if self.first.major > self.second.major:
            result = True
        elif eqmajor and self.first.minor > self.second.minor:
            result = True
        elif eqmajor and eqminor and self.first.patch > self.second.patch:
            result = True
        if not result and self._prereleasegt(0): result = True
        return result

    def lt(self):
        result = False
        eqmajor = self.first.major == self.second.major
        eqminor = self.first.minor == self.second.minor
        if self.first.major < self.second.major:
            result = True
        elif eqmajor and self.first.minor < self.second.minor:
            result = True
        elif eqmajor and eqminor and self.first.patch < self.second.patch:
            result = True
        if not result and self._prereleaselt(0): result = True
        return result

    def ge(self):
        return self.eq() or self.gt()

    def le(self):
        return self.eq() or self.lt()


class Matcher():
    """Class utilizing version matching functionality.

    When matching versions remember that Matcher() will match
    minimal and maximal versions **including** the given ones.
    """
    min, max = None, None
    but = []

    def __init__(self, min=None, max=None, but=[]):
        """To match only one version set the same version to min and
        max.
        In order to match every version except one leave `min` and `max` as
        None and set only `but` parameter.

        :param min: minimal version
        :param max: maximal version
        :param but: match all **but** these versions
        """
        if min is not None: self.min = Version(min)
        if max is not None: self.max = Version(max)
        if but: self.but = [Version(b) for b in but]

    def match(self, version):
        """Returns True if given version matches Matcher() instance.
        """
        version, result = Version(version), False
        min, max = self.min is not None, self.max is not None
        if min and not max:
            result = Comparison(version, self.min).ge()
        elif not min and max:
            result = Comparison(version, self.max).le()
        elif min and max:
            result = Comparison(version, self.min).ge() and Comparison(version, self.max).le()
        elif not min and not max:
            result = True

        if self.but and version in self.but: result = False
        return result


class Version():
    """Object representing version.

    When `tuple()` is made from this Version() object it
    will consist of only version and not prerelease identifiers or
    build metadata.

    `str()` will return only version (without prerelease identifiers or
    build metadata). If you want to have full representation use `repr()`.

    If converted to `bool()` it always returns True.
    """
    string = ''
    major, minor, patch = 0, 0, 0
    prerelease = []
    build = ''

    def __init__(self, string):
        """:param string: version string
        :type string: str
        """
        self.string = string
        if not valid(self.string):
            raise InvalidVersionStringError('invalid version string: {0}'.format(self.string))
        version, prerelease, build = _split(self.string)
        self._setversion(version)
        self._setprerelease(prerelease)
        self._setbuild(build)

    def __eq__(self, v):
        """Checks if two versions are equal.
        """
        return Comparison(self, v).eq()

    def __lt__(self, v):
        """Compares another version.
        :param v: version object
        :type v: semver.version.Version
        """
        return Comparison(self, v).lt()

    def __gt__(self, v):
        """Compares another version.
        :param v: version object
        :type v: semver.version.Version
        """
        return Comparison(self, v).gt()

    def __ge__(self, v):
        """Compares another version.
        :param v: version object
        :type v: semver.version.Version
        """
        return Comparison(self, v).ge()

    def __str__(self):
        """Returns only version (without prerelease or
        build metadata).
        To get string representation with more info use repr().
        """
        return '{0}.{1}.{2}'.format(self.major, self.minor, self.patch)

    def __repr__(self):
        """Returns version, prerelease and build metadata.
        To get only version use str().
        """
        final = str(self)
        if self.prerelease:
            final += '-'
            for i in self.prerelease: final += '{0}.'.format(i)
            final = final[:-1]
        if self.build: final += '+{0}'.format(self.build)
        return final

    def __bool__(self):
        """Always True.
        """
        return True

    def __iter__(self):
        """Iterates over everything - version and prerelease.
        """
        version = [self.major, self.minor, self.patch] + self.prerelease
        return iter(version)

    def __getitem__(self, n):
        """Returns items only from version and
        not prerelease identifiers or
        build metadata.
        """
        if n == 0: item = self.major
        elif n == 1: item = self.minor
        elif n == 2: item = self.patch
        else: raise IndexError('index out of range')
        return item

    def _setversion(self, version):
        """Sets version.
        :param version: version string (e.g.: 3.9.2)
        :type version: str
        """
        version = version.split('.')
        self.major = int(version[0])
        self.minor = int(version[1])
        self.patch = int(version[2])

    def _setprerelease(self, prerelease):
        """Sets prerelease.
        :param prerelease: prerelease string (e.g.: alpha.1.release.3)
        :type prerelease: str
        """
        if prerelease: prerelease = prerelease.split('.')
        else: prerelease = []

        for i in range(len(prerelease)):
            identifier = prerelease[i]
            if not re.match(valid_identifier_regexp, identifier):
                raise InvalidIdentifierError('invalid identifier (part {0}): {1}'.format(i+1, identifier))
            if identifier.isdecimal(): identifier = int(identifier)
            prerelease[i] = identifier
        self.prerelease = prerelease

    def _setbuild(self, build):
        """Sets build metadata.
        :param build: build metadata (build.0.commit.5f265c)
        :type build: str
        """
        self.build = build

    def satisfies(self, min=None, max=None, but=[]):
        """Returns True if this version satisfies requirements
        set as arguments.
        To match only one version set the same version to min and
        max.

        :param min: minimal version
        :param max: maximal version
        :param but: match all **but** these versions
        """
        return Matcher(min=min, max=max, but=but).match(repr(self))
