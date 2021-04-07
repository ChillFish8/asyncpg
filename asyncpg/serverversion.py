# Copyright (C) 2016-present the asyncpg authors and contributors
# <see AUTHORS file>
#
# This module is part of asyncpg and is released under
# the Apache 2.0 License: http://www.apache.org/licenses/LICENSE-2.0


from . import types


def split_server_version_string(version_string):
    version_string = version_string.strip()
    if version_string.startswith('PostgreSQL '):
        version_string = version_string[len('PostgreSQL '):]
    if version_string.startswith('Postgres-XL'):
        version_string = version_string[len('Postgres-XL '):]

    # Some distros (e.g Debian) like may inject their branding
    # into the numeric version string, so make sure to only look
    # at stuff before the first space.
    version_string = version_string.split(' ')[0]
    parts = version_string.strip().split('.')
    if not parts[-1].isdigit():
        # release level specified
        lastitem = parts[-1]
        levelpart = lastitem.rstrip('0123456789').lower()
        if levelpart != lastitem:
            serial = int(lastitem[len(levelpart):])
        else:
            serial = 0

        level = levelpart.lstrip('0123456789')
        if level != levelpart:
            parts[-1] = levelpart[:-len(level)]
        else:
            parts[-1] = 0
    else:
        level = 'final'
        serial = 0

    if int(parts[0]) >= 10:
        # Since PostgreSQL 10 the versioning scheme has changed.
        # 10.x really means 10.0.x.  While parsing 10.1
        # as (10, 1) may seem less confusing, in practice most
        # version checks are written as version[:2], and we
        # want to keep that behaviour consistent, i.e not fail
        # a major version check due to a bugfix release.
        parts.insert(1, 0)

    major, *rest = parts[:3]
    if len(rest) > 0:
        minor, *rest = rest
    else:
        minor = 0

    if len(rest) > 0 and rest[0].isdigit():
        micro, _ = rest
    else:
        micro = 0

    versions = [major, minor, micro, level, serial]

    return types.ServerVersion(*versions)
