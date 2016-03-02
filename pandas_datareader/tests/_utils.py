import nose


def _skip_if_no_lxml():
    try:
        import lxml  # noqa
    except ImportError:  # pragma: no cover
        raise nose.SkipTest("no lxml")


def _get_session(expire_after=None):
    try:
        import requests_cache
        import datetime
        if expire_after is None:
            expire_after = datetime.timedelta(hours=2)
        session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
    except ImporError:
        import requests
        session = requests.Session()
    return session


def _get_logger():
    import logging
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
