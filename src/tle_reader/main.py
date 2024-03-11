import datetime
from dataclasses import dataclass
from typing import Sequence, Tuple

from tle_reader.typing import Classification
from tle_reader.utils import (
    alpha5_to_number,
    epoch_to_datetime,
    number_to_alpha5,
    scinot_to_float,
)

# Line 1
# Columns 	Example 	Description
# 1 	1 	Line Number
# 3-7 	25544 	Satellite Catalog Number
# 8 	U 	Elset Classification
# 10-17 	98067A 	International Designator
# 19-32 	04236.56031392 	Element Set Epoch (UTC) *Note: spaces are acceptable in columns 21 & 22
# 34-43 	.00020137 	1st Derivative of the Mean Motion with respect to Time
# 45-52 	00000-0 	2nd Derivative of the Mean Motion with respect to Time (decimal point assumed)
# 54-61 	16538-3 	B* Drag Term
# 63 	0 	Element Set Type
# 65-68 	999 	Element Number
# 69 	3 	Checksum
# Line 2
# Columns 	Example 	Description
# 1 	2 	Line Number
# 3-7 	25544 	Satellite Catalog Number
# 9-16 	51.6335 	Orbit Inclination (degrees)
# 18-25 	344.7760 	Right Ascension of Ascending Node (degrees)
# 27-33 	0007976 	Eccentricity (decimal point assumed)
# 35-42 	126.2523 	Argument of Perigee (degrees)
# 44-51 	325.9359 	Mean Anomaly (degrees)
# 53-63 	15.70406856 	Mean Motion (revolutions/day)
# 64-68 	32890 	Revolution Number at Epoch
# 69 	6 	Checksum)


def compute_checksum(line: str) -> int:
    cs = 0
    for v in line:
        if v in "-":
            cs += -1
        elif v.isnumeric():
            cs += int(v)
    return cs % 10


def read_tle(line1: str, line2: str) -> Tuple[str]:
    catalog1 = alpha5_to_number(line1[2:7])
    classification = line1[7]
    intl_des = line1[9:17]
    epoch = epoch_to_datetime(line1[18:32])
    Md = float(line1[33:43])
    Mdd = scinot_to_float(line1[44:52])
    Bstar = scinot_to_float(line1[53:61])
    elset_type = int(line1[62])
    element_number = int(line1[64:68])
    checksum1 = int(line1[68])

    catalog2 = alpha5_to_number(line2[2:7])
    i = float(line2[8:16])
    r = float(line2[17:25])
    e = float(line2[26:33])
    p = float(line2[34:42])
    mu = float(line2[43:51])
    M = float(line2[52:63])
    revnum = int(line2[63:68])
    checksum2 = line1[68]

    if catalog1 != catalog2:
        raise ValueError

    return {
        "classification": classification,
        "catalog": catalog1,
        "intl_des": intl_des,
        "epoch": epoch,
        "M": M,
        "Md": Md,
        "Mdd": Mdd,
        "Bstar": Bstar,
        "type": elset_type,
        "number": element_number,
        "i": i,
        "r": r,
        "e": e,
        "p": p,
        "mu": mu,
        "revolution_number": revnum,
    }


@dataclass
class TLE:
    catalog: int
    """Satellite Catalog Number (Integer Notation)"""
    classification: Classification
    """Elset Classification"""
    intl_des: str
    """International Designator"""
    epoch: datetime.datetime
    """Element Set Epoch """
    bstar: float
    """B* Drag Term"""
    type: int
    """Element Set Type"""
    number: int
    """Element Number"""
    i: float
    """Inclination (deg)"""
    r: float
    """Right Ascension of the Ascending Node (deg)"""
    e: float
    """Eccentricity"""
    aop: float
    """Argument of Perigee (deg)"""
    mu: float
    """Mean Anomaly (deg)"""
    M: float
    """Mean Motion (rev/day)"""
    Md: float
    """Mean Motion 1st Derivative (rev/day^2)"""
    Mdd: float
    """Mean Motion 2nd Derivative (rev/day^3)"""
    rev_num: int
    """Revolution Number at Epoch"""

    @property
    def alpha5(self) -> str:
        """Satellite Catalog Number (Alpha-5 Notation)"""
        return number_to_alpha5(self.catalog)

    @property
    def line1(self) -> str:
        """TLE Line 1"""

    @property
    def line2(self) -> str:
        """TLE Line 2"""

    @classmethod
    def from_lines(cls, lines: Sequence[str]) -> "TLE":
        pass
