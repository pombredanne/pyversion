#!/usr/bin/env python3

import unittest
from semver.version import Version, Comparison, valid


#   if set to True tests will be verbose
DEBUG = False


versions_to_compare_lt = [  ('2.0.0', '3.0.0', True),
                            ('3.0.1', '3.1.0', True),
                            ('3.0.0', '3.0.1', True),
                            ('3.2.1-alpha', '3.2.1-alpha.1', True),
                            ('3.2.1-alpha.1', '3.2.1-beta', True),
                            ('3.2.1-beta', '3.2.1-beta.4', True),
                            ('3.2.1-beta.4', '3.2.1-beta.17', True),
                            ('3.2.1-beta.17', '3.2.1-rc.8', True),
                            ('3.2.1-rc.8', '3.2.1-rc.12', True),
                            ('3.2.1', '3.2.2-alpha.1', True),
                            ('3.2.3-rc.8', '3.2.3-rel.1', True),
                            ('3.2.3-rc.8', '3.2.3-release.1', True),
                            ('3.2.1+7', '3.2.2+6', True),
                            ('6.4.8-a.3+17', '6.4.8-a.4+2', True),
                            ('6.4.8', '6.40.8', True),
                            ('3.2.1-rc.8', '3.2.1', True),
                            ('3.2.1-alpha.1', '3.2.1-alpha.1.rel.3', True),
                            ('0.0.2', '0.0.1', False),
                            ]

versions_to_compare_gt = [  ('3.0.0', '2.0.0', True),
                            ('3.1.0', '3.0.1', True),
                            ('3.1.1', '3.1.0', True),
                            ('3.0.1', '3.0.0-alpha', True),
                            ('3.0.0-alpha.1', '3.0.0-alpha', True),
                            ('3.0.0-beta', '3.0.0-alpha.1', True),
                            ('3.0.0-beta.1', '3.0.0-beta', True),
                            ('3.0.0-rc', '3.0.0-beta.1', True),
                            ('3.0.0-rc.1', '3.0.0-rc', True),
                            ('3.0.0-release', '3.0.0-rc.1', True),
                            ('0.0.3', '0.1.0-rc.1', True),
                            ('0.0.2', '0.0.1', True),
                            ('0.0.1', '0.0.2', False),
                            ]

versions_to_compare_ge = [  ('3.2.1', '3.2.1'),
                            ('3.2.2', '3.2.1'),
                            ('3.3.6-rc.7', '3.3.6-rc.5'),
                            ]

versions_to_compare_le = [  ('2.0.0', '3.0.0'),
                            ('2.0.0', '2.0.0'),
                            ('3.0.0', '3.0.1'),
                            ('3.0.0-alpha', '3.0.0-alpha.1'),
                            ('3.0.0-alpha.2', '3.0.0-alpha.2'),
                            ('3.0.0-rc.7', '3.1.0-alpha.2'),
                            ]

class ComparisonTests(unittest.TestCase):
    def testLesserThan(self):
        for l, g, result in versions_to_compare_lt:
            if DEBUG: print(l, g)
            self.assertEqual(result, Comparison(Version(l), Version(g)).lt())
            self.assertEqual(result, Version(l) < Version(g))

    def testGreaterThan(self):
        for g, l, result in versions_to_compare_gt:
            if DEBUG: print(g, l)
            self.assertEqual(result, Comparison(Version(g), Version(l)).gt())
            self.assertEqual(result, Version(g) > Version(l))

    def testGreaterOrEqual(self):
        for x, y in versions_to_compare_ge:
            self.assertEqual(True, Comparison(Version(x), Version(y)).ge())
            self.assertEqual(True, Version(x) >= Version(y))

    def testLesserOrEqual(self):
        for x, y in versions_to_compare_le:
            if DEBUG: print(x, y)
            self.assertEqual(True, Comparison(Version(x), Version(y)).le())
            self.assertEqual(True, Version(x) <= Version(y))


class InitializationTests(unittest.TestCase):
    def testOnlyVersion(self):
        v = Version('3.9.3')
        self.assertEqual(3, v.major)
        self.assertEqual(9, v.minor)
        self.assertEqual(3, v.patch)

    def testVersionAndPrerelease(self):
        v = Version('3.9.3-alpha.1.release.3')
        self.assertEqual(3, v.major)
        self.assertEqual(9, v.minor)
        self.assertEqual(3, v.patch)
        self.assertEqual(['alpha', 1, 'release', 3], v.prerelease)

    def testBuildMetadata(self):
        v1 = Version('3.9.3-alpha.1+42')
        v2 = Version('3.9.3+42')
        self.assertEqual('42', v1.build)
        self.assertEqual('42', v2.build)


class SatisfactionTests(unittest.TestCase):
    def testMinimal(self):
        v = Version('3.2.1')
        self.assertEqual(True, v.satisfies(min='3.0.0'))

    def testMaximal(self):
        v = Version('1.8.12')
        self.assertEqual(True, v.satisfies(max='1.8.12'))
    
    def testBetween(self):
        v = Version('3.2.1-rc.8')
        self.assertEqual(True, v.satisfies(min='3.2.1-alpha.1', max='3.2.1-rc.12'))

    def testExcept(self):
        v = Version('3.2.1-rc.8')
        self.assertEqual(False, v.satisfies(but=['3.2.1-rc.8']))

    def testAll(self):
        v = Version('3.2.1-rc.8')
        self.assertEqual(True, v.satisfies())


class StringTests(unittest.TestCase):
    def testStr(self):
        v = Version('3.9.3-release.4+build.42')
        if DEBUG: print(str(v))
        self.assertEqual('3.9.3', str(v))

    def testRepr(self):
        v = Version('3.9.3-release.4+build.42')
        if DEBUG: print(repr(v))
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
            self.assertEqual(True, valid(i))

    def testInvalid(self):
        vs = [  '3.2.1.2',
                '3.9.2-alpha.1.?.release.5',
                '3.9.c',
                ]
        for i in vs:
            self.assertEqual(False, valid(i))


if __name__ == '__main__': unittest.main()
