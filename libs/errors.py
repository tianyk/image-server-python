#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tyk'


class DoogError(Exception):
    """Base class for all Doog exceptions.
    """


class InvalidRequestError(DoogError):
    def __init__(self, param, msg, value):
        self.param = param
        self.msg = msg
        self.value = value


