import datetime
import re

ALPHA5_MAP = {v: i for i, v in enumerate("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ")}
ALPHA5_MAP_REV = {i: v for v, i in ALPHA5_MAP.items()}


def alpha5_to_number(value: str) -> int:
    """Convert an Alpha-5 number to an integer"""
    if value.isnumeric():
        return int(value)
    return ALPHA5_MAP[value[0]] * 10_000 + int(value[1:])


def number_to_alpha5(value: int) -> str:
    """Convert an integer to an Alpha-5 number"""
    if value < 10_000:
        return f"{value:5}"
    quotient, remainder = divmod(value, 10_000)
    letter = ALPHA5_MAP_REV[quotient]
    return f"{letter}{remainder:04}"


# Field 	Columns 	Content 	Example
# 1 	01 	Line number 	1
# 2 	03–07 	Satellite catalog number 	25544
# 3 	08 	Classification (U: unclassified, C: classified, S: secret) [12] 	U
# 4 	10–11 	International Designator (last two digits of launch year) 	98
# 5 	12–14 	International Designator (launch number of the year) 	067
# 6 	15–17 	International Designator (piece of the launch) 	A
# 7 	19–20 	Epoch year (last two digits of year) 	08
# 8 	21–32 	Epoch (day of the year and fractional portion of the day) 	264.51782528
# 9 	34–43 	First derivative of mean motion; the ballistic coefficient [13] 	-.00002182
# 10 	45–52 	Second derivative of mean motion (decimal point assumed) [13] 	00000-0
# 11 	54–61 	B*, the drag term, or radiation pressure coefficient (decimal point assumed) [13] 	-11606-4
# 12 	63–63 	Ephemeris type (always zero; only used in undistributed TLE data) [14] 	0
# 13 	65–68 	Element set number. Incremented when a new TLE is generated for this object.[13] 	292
# 14 	69 	Checksum (modulo 10) 	7

EPOCH_TIME_RESOLUTION = 0.00000001 * 86_400


def epoch_to_datetime(value: str) -> datetime.datetime:
    yy = int(value[0:2]) + 1900
    if yy < 1957:
        yy += 100
    jday = float(value[2:14]) - 1
    return datetime.datetime(yy, 1, 1) + datetime.timedelta(days=jday)


def datetime_to_epoch(value: datetime.datetime) -> str:
    day = datetime.datetime(value.year, value.month, value.day)
    tod = value - day
    yy_jday = int(value.strftime("%y%j"))
    epoch = yy_jday + tod.total_seconds() / 86_400
    return f"{epoch:014.8f}"


def scinot_to_float(s: str) -> float:
    """Convert implied decimal scientific notation to a Python float."""
    return float(s[0] + "." + s[1:6] + "e" + s[6:8])


def float_to_scinot(value: float) -> str:
    """Convert a Python float to implied decimal scientific notation."""
    tmp = f"{value*10: 10.4e}"
    tmp = tmp[0:9] + tmp[10:11]
    return tmp.replace(".", "").replace("e", "").replace("+0", "-0")


def e_to_float(value: str) -> float:
    return float("." + value)


def float_to_e(value: float) -> str:
    return f"{value:.7f}"[-7:]
