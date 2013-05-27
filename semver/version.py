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

    def _lesseridentifiers(self, fidentifiers):
        result = True
        for i, t in enumerate(zip(self.identifiers, fidentifiers)):
            local, foreign = t
            if local > foreign and not self._lesseridentifiers(fidentifiers[i+1:]):
                result = False
                break
        return result

    def __eq__(self, v):
        """Checks if two versions are equal.
        """
        result = False
        if (self.major == v.major and self.minor == v.minor and 
            self.patch == v.patch and self.identifiers == v.identifiers):
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
            if not self._lesseridentifiers(v.identifiers): result = False
        return result

    def __str__(self):
        """Returns only version (without identifiers or
        build metadata).
        To get string representation with more info use repr().
        """
        return '{0}.{1}.{2}'.format(self.major, self.minor, self.patch)

    def __repr__(self):
        """Returns version, identifiers and build metadata.
        To get only version use str().
        """
        final = str(self)
        if self.identifiers:
            final += '-'
            for i in self.identifiers: final += '{0}.'.format(i)
            final = final[:-1]
        if self.build: final += '+{0}'.format(self.build)
        return final

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
        else: identifiers = []

        for i in range(len(identifiers)):
            identifier = identifiers[i]
            if re.match(valid_identifier_regexp, identifier) is None:
                raise InvalidIdentifierError('invalid identifier (part {0}): {1}'.format(i+1, identifier))
            if identifier.isdecimal(): identifier = int(identifier)
            identifiers[i] = identifier
        self.identifiers = identifiers

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
