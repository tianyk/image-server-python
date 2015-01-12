#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def split_host_and_port(netloc):
    """Returns ``(host, port)`` tuple from ``netloc``.

    Returned ``port`` will be ``None`` if not present.
    """
    match = re.match(r'^(.+):(\d+)$', netloc)
    if match:
        host = match.group(1)
        port = int(match.group(2))
    else:
        host = netloc
        port = None
    return (host, port)


uri = "http://localhost:8080/photos/1234.jpg?w=200&h=200"

for x in split_host_and_port(uri):
    print x