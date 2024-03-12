import datetime

import pytest
from tle_reader.main import read_tle
from tle_reader.utils import (
    EPOCH_TIME_RESOLUTION,
    alpha5_to_number,
    compute_checksum,
    datetime_to_epoch,
    epoch_to_datetime,
    float_to_implied_decimal,
    float_to_scinot,
    implied_decimal_to_float,
    number_to_alpha5,
    scinot_to_float,
)


@pytest.mark.parametrize(
    "number, alpha5",
    [
        (100000, "A0000"),
        (148493, "E8493"),
        (182931, "J2931"),
        (234018, "P4018"),
        (301928, "W1928"),
        (339999, "Z9999"),
    ],
)
class TestAlpha5ToNumber:
    def test_alpha5_to_number(self, number: int, alpha5: str):
        assert alpha5_to_number(alpha5) == number

    def test_number_to_alpha5(self, number: int, alpha5: str):
        assert alpha5 == number_to_alpha5(number)


@pytest.mark.parametrize(
    "dt_string, epoch",
    [
        ("1957-01-01T00:00:00.000", "57001.00000000"),
        ("2001-01-01T00:00:00.000", "01001.00000000"),
        ("2056-12-31T00:00:00.000", "56366.00000000"),  # leap year
        ("2020-01-01T12:00:00.000", "20001.50000000"),
        ("2020-09-30T10:07:00.000", "20274.42152778"),
        # (),
        # (),
    ],
)
class TestEpoch:
    def test_epoch_to_datetime(self, dt_string: str, epoch: str):
        dt = datetime.datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S.%f")
        error = dt - epoch_to_datetime(epoch)
        assert abs(error.total_seconds()) <= EPOCH_TIME_RESOLUTION

    def test_datetime_to_epoch(self, dt_string: str, epoch: str):
        dt = datetime.datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S.%f")
        assert datetime_to_epoch(dt) == epoch


@pytest.mark.parametrize(
    "scinot, value",
    [
        (" 10000-0", 0.1),
        (" 00000-0", 0.0),
        (" 16538-3", 0.16538e-3),
    ],
)
class TestSciNot:
    def test_scinot_to_float(self, scinot: str, value: float):
        assert scinot_to_float(scinot) == pytest.approx(value)

    def test_float_to_scinot(self, scinot: str, value: float):
        print(value, float_to_scinot(value))
        assert float_to_scinot(value) == scinot


@pytest.mark.parametrize(
    "line",
    [
        "1 25544U 98067A   04236.56031392  .00020137  00000-0  16538-3 0  9993",
        "2 25544  51.6335 344.7760 0007976 126.2523 325.9359 15.70406856328906",
    ],
)
class TestChecksum:
    def test_compute_checksum(self, line):
        assert compute_checksum(line) == int(line[68])


@pytest.mark.parametrize(
    "idec, value",
    [
        ("1234567", 0.1234567),
        ("0007976", 0.0007976),
    ],
)
class TestImpliedDecimal:
    def test_implied_decimal_to_float(self, idec: str, value: float):
        assert implied_decimal_to_float(idec) == pytest.approx(value)

    def test_float_to_implied_decimal(self, idec: str, value: float):
        assert float_to_implied_decimal(value) == idec


@pytest.mark.parametrize(
    "line1, line2",
    [
        (
            "1 25544U 98067A   04236.56031392  .00020137  00000-0  16538-3 0  9993",
            "2 25544  51.6335 344.7760 0007976 126.2523 325.9359 15.70406856328906",
        ),
    ],
)
class TestParser:
    def test_parse_checksum(self, line1, line2):
        tle = read_tle(line1, line2)
        assert tle
