from setuptools import setup, Extension

setup(
    name="fciso8601",
    version="1.0.1",
    description='Fast ISO8601 date time parser for Python written in C',
    ext_modules=[Extension("fciso8601", ["module.c"])],
    test_suite='tests',
    tests_require=['pytz'],
)
