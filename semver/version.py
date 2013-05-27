#!/usr/bin/env python3


import re


"""This is main module for semver.py - Semantic Versioning
library for Python3 language.
"""


__version__ = '0.0.1'


valid_identifier_regexp = re.compile('^[0-9A-Za-z-]*$')
base_regexp =   ('[0-9]+\.[0-9]+\.[0-9]+'                   #   major.minor.patch
                '(-([0-9A-Za-z-]+)(\.[0-9A-Za-z-]+)*)?'     #   prerelease
                '(\+([0-9A-Za-z-]+)(\.[0-9A-Za-z-]+)*)?')   #   build
match_regexp = re.compile('^{0}$'.format(base_regexp))


class InvalidVersionStringError(Exception):
    pass


class InvalidIdentifierError(Exception):
    pass


def _prerelzip(a, b):
    """Zips two prerelease lists.
    If one is longer it will not truncate but
    will fill with zeros.
    """
    n = max(len(a), len(b))
    zipped = []
    for i in range(n):
        try: m = a[i]
        except IndexError: m = 0
        finally: pass
        try: n = b[i]
        except IndexError: n = 0
        finally: pass
        zipped.append( (m, n) )
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

    def _lesserprerelease(self, fprerelease, n=0):
        """Compares prerelease identifiers.
        :param fprerelease: prerelease identifiers list
        """
        result = True
        for i, t in enumerate(_prerelzip(self.prerelease[n:], fprerelease[n:])):
            local, foreign = t
            try:
                comparison = local > foreign
            except TypeError:
                if type(local) == int: comparison = True
                elif type(foreign) == int: comparison = False
            finally:
                if comparison and not self._lesserprerelease(fprerelease, n=i+1): result = False
            if not result: break
        return result

    def __eq__(self, v):
        """Checks if two versions are equal.
        """
        result = False
        if (self.major == v.major and self.minor == v.minor and 
            self.patch == v.patch and self.prerelease == v.prerelease):
            result = True
        return result

    def __lt__(self, v):
        """Compares another version.
        :param v: version object
        :type v: semver.version.Version
        """
        result = True
        if self.major > v.major:
            result = False
        elif self.major == v.major and self.minor > v.minor:
            result = False
        elif self.major == v.major and self.minor == v.minor and self.patch > v.patch:
            result = False
        elif self.major == v.major and self.minor == v.minor and self.patch == v.patch:
            if not self._lesserprerelease(v.prerelease): result = False
        return result

    def __le__(self, v):
        """Less or equal.
        """
        return self.__eq__(v) or self.__lt__(v)

    def __ge__(self, v):
        """Greater or equal.
        """
        return self.__eq__(v) or self.__gt__(v)

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
            if re.match(valid_identifier_regexp, identifier) is None:
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

    def _analyze(self, version, prerelease='', build=''):
        """Analyzes version data.
        """
        self._setversion(version)
        self._setprerelease(prerelease)
        self._setbuild(build)

    def satisfies(self, min=None, max=None, but=[]):
        """Returns True if this version satisfies requirements
        set as arguments.
        To match only one version set the same version to min and
        max.

        :param min: minimal version
        :param max: maximal version
        :param but: match all **but** these versions
        """
        result = False
        if min is not None and max is None:
            result = self > Version(min)
        elif min is None and max is not None:
            result = self < Version(max)
        elif min is not None and max is not None:
            result = self > Version(min) and self < Version(max)

        if but:
            but = [Version(v) for v in but]
            if self in but: result = False
        return result
