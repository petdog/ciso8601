ciso8601
========

`ciso8601` converts ISO8601 date time strings into Python datetime objects. Since it's written as a C module, it is much faster than other Python libraries.

Usage
-----

```
% pip install ciso8601
```

```
In [1]: import ciso8601

In [2]: ciso8601.parse_datetime('2014-12-05T12:30:45.123456-05:30')
Out[2]: datetime.datetime(2014, 12, 5, 12, 30, 45, 123456, tzinfo=pytz.FixedOffset(330))

In [3]: ciso8601.parse_datetime('20141205T123045')
Out[3]: datetime.datetime(2014, 12, 5, 12, 30, 45)

In [4]: ciso8601.parse_datetime_unaware('2014-12-05T12:30:45.123456-05:30')
Out[4]: datetime.datetime(2014, 12, 5, 12, 30, 45, 123456)
```

Benchmark
---------

Date time string with no time zone information:
```
In [1]: import datetime, aniso8601, iso8601, isodate, dateutil.parser, arrow, ciso8601

In [2]: ds = u'2014-01-09T21:48:00.921000'

In [3]: %timeit ciso8601.parse_datetime(ds)
1000000 loops, best of 3: 320 ns per loop

In [4]: %timeit datetime.datetime.strptime(ds, "%Y-%m-%dT%H:%M:%S.%f")
100000 loops, best of 3: 19.7 us per loop

In [5]: %timeit dateutil.parser.parse(ds)
10000 loops, best of 3: 111 us per loop

In [6]: %timeit aniso8601.parse_datetime(ds)
10000 loops, best of 3: 31.1 us per loop

In [7]: %timeit iso8601.parse_date(ds)
10000 loops, best of 3: 70.9 us per loop

In [8]: %timeit isodate.parse_datetime(ds)
10000 loops, best of 3: 81.8 us per loop

In [9]: %timeit arrow.get(ds).datetime
10000 loops, best of 3: 41.4 us per loop
```

ciso8601 takes 0.32us, which is 62x faster than datetime's strptime, which is not a full ISO8601 parser. It is **97x faster than aniso8601**, the next fastest ISO8601 parser in this comparison.

Date time string with time zone information:

```
In [1]: import datetime, aniso8601, iso8601, isodate, dateutil.parser, arrow, ciso8601

In [2]: ds = u'2014-01-09T21:48:00.921000+05:30'

In [3]: %timeit ciso8601.parse_datetime(ds)
100000 loops, best of 3: 3.62 us per loop

In [4]: %timeit dateutil.parser.parse(ds)
10000 loops, best of 3: 126 us per loop

In [5]: %timeit aniso8601.parse_datetime(ds)
10000 loops, best of 3: 34.9 us per loop

In [6]: %timeit iso8601.parse_date(ds)
10000 loops, best of 3: 94 us per loop

In [7]: %timeit isodate.parse_datetime(ds)
10000 loops, best of 3: 91.3 us per loop

In [8]: %timeit arrow.get(ds).datetime
10000 loops, best of 3: 56.2 us per loop
```

Even with time zone information, `ciso8601` is almost 10x faster than `aniso8601`.

Tested on Python 2.7 on OS X 10.9.2 using the following modules:

```
aniso8601==0.82
arrow==0.4.2
ciso8601==1.0
iso8601==0.1.10
isodate==0.5.0
python-dateutil==2.2
```

Supported formats
-----------------

Dates may have one of the following formats:
* `YYYYMMDD`
* `YYYY-MM-DD`
* `YYYY-MM`

Week dates or ordinal dates are not currently supported.

Times are optional and are separated by the letter `T` or also by space (unlike ISO8601). The following time formats are supported:
* `hh`
* `hhmm` or `hh:mm`
* `hhmmss` or `hh:mm:ss`

Fractions of a second may be provided, separated by `.` or `,`. Up to 6 digits are supported, excessive digits will be ignored.

Time zone information may be provided in one of the following formats:
* `Z`
* `±hh`
* `±hh:mm`
* `±hhmm`

If time zone information is provided, an aware datetime object will be returned. Otherwise, the datetime is unaware. Please note that it takes more time to parse aware datetimes, especially if they're not in UTC. If you don't care about time zone information, use the `parse_datetime_unaware` method, which will discard any time zone information and is faster. Parsing aware date times requires the `pytz` module, otherwise time zone information is ignored and unaware datetimes are returned.

If parsing fails, `None` will be returned. The parser will attempt to parse as much of the date time as possible.
