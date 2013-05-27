#!/usr/bin/env python3


import re


"""This is main module for semver.py - Semantic Versioning
library for Python3 language.
"""


__version__ = '0.0.1'


valid_identifier_regexp = re.compile('^[0-9A-Za-z-]*$')
valid_verstring_regexp = re.compile('[0-9]+\.[0-9]+\.[0-9]+(-([0-9A-Za-z-].?)+)?(\+[0-9A-Za-z-]+)?')


class InvalidVersionStringError(Exception):
    pass


class InvalidIdentifierError(Exception):
    pass


def split(string):
    """Splits version string into main version,
    identifiers and build metadata.
    """
    version, identifiers, build = '', '', ''
    if re.match(valid_verstring_regexp, string) is None:
        raise InvalidVersionStringError(string)

    if '-' in string:
        n = string.index('-')
        version = string[:n]
        identifiers = string[n+1:]
    else:
        version = string
    if '+' in identifiers:
        n = identifiers.rindex('+')
        build = identifiers[n+1:]
        identifiers = identifiers[:n]
    if '+' in version:
        n = version.rindex('+')
        build = version[n+1:]
        version = version[:n]
    return (version, identifiers, build)


class Version():
    """Object representing version.
    """
    string = ''
    major, minor, patch = 0, 0, 0
    identifiers = []
    build = ''

    def __init__(self, string):
        """:param string: version string
        :type string: str
        """
        self.string = string
        version, identifiers, build = split(self.string)
        self._analyze(version, identifiers, build)

    def _setversion(self, version):
        """Sets version.
        :param version: version string (e.g.: 3.9.2)
        :type version: str
        """
        version = version.split('.')
        self.major = int(version[0])
        self.minor = int(version[1])
        self.patch = int(version[2])

    def _setidentifiers(self, identifiers):
        """Sets identifiers.
        :param identifiers: identifiers string (e.g.: alpha.1.release.3)
        :type identifiers: str
        """
        if identifiers: identifiers = identifiers.split('.')

        for i in range(len(self.identifiers)):
            identifier = self.identifiers[i]
            if re.match(valid_identifier_regexp, identifier) is None:
                raise InvalidIdentifierError('invalid identifier (part {0}): {1}'.format(i+1, identifier))
            if identifier.isdecimal(): self.identifiers[i] = int(identifier)

    def _setbuild(self, build):
        """Sets build metadata.
        :param build: build metadata (build.0.commit.5f265c)
        :type build: str
        """
        self.build = build

    def _analyze(self, version, identifiers='', build=''):
        """Analyzes version data.
        :param vt: version tuple (version, identifiers) returned by split()
        :type vt: tuple
        """
        self._setversion(version)
        self._setidentifiers(identifiers)
        self._setbuild(build)
