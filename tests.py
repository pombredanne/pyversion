#!/usr/bin/env python3

import unittest
import semver


versions_to_compare_lt = [  ('3.2.3', '3.2.4'),
                            ('3.2.1-alpha', '3.2.1-alpha.1'),
                            ('3.2.1-alpha.1', '3.2.1-beta'),
                            ('3.2.1-beta', '3.2.1-beta.4'),
                            ('3.2.1-beta.4', '3.2.1-beta.17'),
                            ('3.2.1-beta.17', '3.2.1-rc.8'),
                            ('3.2.1-rc.8', '3.2.1-rc.12'),
                            ('3.2.1', '3.2.2-alpha.1'),
                            ('3.2.3-rc.8', '3.2.3-rel.1'),
                            ('3.2.3-rc.8', '3.2.3-release.1'),
                            ('3.2.1+7', '3.2.2+6'),
                            ('6.4.8-a.3+17', '6.4.8-a.4+2'),
                            ('6.4.8', '6.40.8'),
                            ('3.2.1-rc.8', '3.2.1'),
                            ('3.2.1-alpha.1', '3.2.1-alpha.1.rel.3'),
                            ]

versions_to_compare_gt = [  ('3.3.0', '3.2.4'),
                            ('3.3.1-alpha.1', '3.3.1-alpha'),
                            ('2.9.8-rc.7', '2.9.8-beta.14'),
                            ('15.0.1-beta.4', '15.0.1-b.2'),
                            ('16.12.47-release.1', '16.12.47-beta.12'),
                            ]

versions_to_compare_ge = [  ('3.2.1', '3.2.1'),
                            ('3.2.2', '3.2.1'),
                            ('3.3.6-rc.7', '3.3.6-rc.5'),
                            ]

class ComparisonTests(unittest.TestCase):
    def testLesserThan(self):
        for l, g in versions_to_compare_lt:
            self.assertEqual(True, semver.version.Version(l) < semver.version.Version(g))

    def testGreaterThan(self):
        for g, l in versions_to_compare_gt:
            self.assertEqual(True, semver.version.Version(g) > semver.version.Version(l))

    def testGreaterOrEqual(self):
        for x, y in versions_to_compare_ge:
            self.assertEqual(True, x >= y)


class InitializationTests(unittest.TestCase):
    def testOnlyVersion(self):
        v = semver.version.Version('3.9.3')
        self.assertEqual(3, v.major)
        self.assertEqual(9, v.minor)
        self.assertEqual(3, v.patch)

    def testVersionAndPrerelease(self):
        v = semver.version.Version('3.9.3-alpha.1.release.3')
        self.assertEqual(3, v.major)
        self.assertEqual(9, v.minor)
        self.assertEqual(3, v.patch)
        self.assertEqual(['alpha', 1, 'release', 3], v.prerelease)

    def testBuildMetadata(self):
        v1 = semver.version.Version('3.9.3-alpha.1+42')
        v2 = semver.version.Version('3.9.3+42')
        self.assertEqual('42', v1.build)
        self.assertEqual('42', v2.build)


class SatisfactionTests(unittest.TestCase):
    def testMinimal(self):
        v = semver.version.Version('3.2.1')
        self.assertEqual(True, v.satisfies(min='3.0.0'))

    def testMaximal(self):
        v = semver.version.Version('1.8.12')
        self.assertEqual(True, v.satisfies(max='1.8.12'))
    
    def testBetween(self):
        v = semver.version.Version('3.2.1-rc.8')
        self.assertEqual(True, v.satisfies(min='3.2.1-alpha.1', max='3.2.1-rc.12'))


class StringTests(unittest.TestCase):
    def testStr(self):
        v = semver.version.Version('3.9.3-release.4+build.42')
        print(str(v))
        self.assertEqual('3.9.3', str(v))

    def testRepr(self):
        v = semver.version.Version('3.9.3-release.4+build.42')
        print(repr(v))
        self.assertEqual('3.9.3-release.4+build.42', repr(v))


class ValidationTests(unittest.TestCase):
    def testValid(self):
        vs = [  '3.2.1',
                '13.29.42',
                '3.9.2-alpha.1.release.5',
                '3.9.2+42',
                '3.9.2-rc.6+2',
                ]
        for i in vs:
            self.assertEqual(True, semver.version.valid(i))

    def testInvalid(self):
        vs = [  '3.2.1.2',
                '3.9.2-alpha.1.?.release.5',
                '3.9.c',
                ]
        for i in vs:
            self.assertEqual(False, semver.version.valid(i))


if __name__ == '__main__': unittest.main()
