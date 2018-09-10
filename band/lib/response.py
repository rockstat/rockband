from ..constants import RESP_META_KEY

RESP_PIXEL = 'pixel'
RESP_REDIRECT = 'redirect'
RESP_ERROR = 'error'


def redirect_response(location, httpCode=302, data={}):
    return {RESP_META_KEY: dict(type=RESP_REDIRECT, location=location, httpCode=httpCode, data=data)}


def pixel_response(data={}):
    return {RESP_META_KEY: dict(type=RESP_PIXEL, data={})}


def error_response(message="", httpCode=500, data={}):
    return {RESP_META_KEY: dict(type=RESP_ERROR, errorMessage=message, httpCode=httpCode, data=data)}


__all__ = ['pixel', 'redirect', 'error']