## Changelog for pyversion library

This file contains history of changes in API of `pyversion` library.


----

#### `0.3.1` (2013-09-20):

This version fixes a bug in comparison logic which is a bit too long to explain in __fix__ note.
The bug was appearing when comparing versions of equal bases but on with prerelease params and
one without. According to standard the one without them is greater -- but `pyversion` said the one
*with* them was greater. Now it's fixed.

* __fix__:  fixed comparison,


----


#### `0.3.0` (2013-09-20):

* __fix__:  fixed comparison for non-standard versions,
* __fix__:  added missing `strict` parameter to `pyversion.version.extract()`


----


#### Version 0.2.0 (2013-08-18):

* __new__:  support for both standard semver version strings and non-standard (shorter, longer),
* __new__:  renamed from `semver` to `pyversion`

