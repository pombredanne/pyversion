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


class ComparisonTests(unittest.TestCase):
    def testCompareOnlyVersion(self):
        lesser = semver.version.Version('3.8.42')
        greater = semver.version.Version('3.9.24')
        self.assertEqual(True, lesser < greater)
        self.assertEqual(True, greater > lesser)
        self.assertEqual(False, greater == lesser)
        self.assertEqual(True, greater != lesser)

    def testCompareVersionsAndIdentifiersLesserToGreater(self):
        versions =  [   ('3.2.1-alpha', '3.2.1-alpha.1'),
                        ('3.2.1-alpha.1', '3.2.1-beta'),
                        ('3.2.1-beta', '3.2.1-beta.4'),
                        ('3.2.1-beta.4', '3.2.1-beta.17'),
                        ('3.2.1-beta.17', '3.2.1-rc.8'),
                        ('3.2.1-rc.8', '3.2.1-rc.12'),
                    ]
        for l, g in versions:
            print(l, g)
            self.assertEqual(True, semver.version.Version(l) < semver.version.Version(g))
            self.assertEqual(True, semver.version.Version(g) > semver.version.Version(l))
            self.assertEqual(False, semver.version.Version(g) == semver.version.Version(l))
            self.assertEqual(True, semver.version.Version(g) != semver.version.Version(l))


if __name__ == '__main__': unittest.main()
