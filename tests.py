#!/usr/bin/env python3

import unittest

import semver


class InitializationTests(unittest.TestCase):
    def testOnlyVersion(self):
        v = semver.version.Version('3.9.3')
        self.assertEqual(3, v.major)
        self.assertEqual(9, v.minor)
        self.assertEqual(3, v.patch)

    def testVersionAndIdentifiers(self):
        v = semver.version.Version('3.9.3-alpha.1.release.3')
        self.assertEqual(3, v.major)
        self.assertEqual(9, v.minor)
        self.assertEqual(3, v.patch)
        self.assertEqual(['alpha', 1, 'release', 3], v.identifiers)

    def testBuildMetadata(self):
        v1 = semver.version.Version('3.9.3-alpha.1+42')
        v2 = semver.version.Version('3.9.3+42')
        self.assertEqual('42', v1.build)
        self.assertEqual('42', v2.build)


if __name__ == '__main__': unittest.main()
