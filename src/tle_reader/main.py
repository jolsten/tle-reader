import datetime
from dataclasses import dataclass
from typing import Tuple

from tle_reader.typing import Classification
from tle_reader.utils import (
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


def parse_tle(line1: str, line2: str) -> Tuple[str]:
    catalog1 = alpha5_to_number(line1[2:7])
    classification = line1[7]
    intl_des = line1[9:17]
    epoch = epoch_to_datetime(line1[18:32])
    nd = float(line1[33:43])
    ndd = scinot_to_float(line1[44:52])
    Bstar = scinot_to_float(line1[53:61])
    elset_type = int(line1[62])
    element_number = int(line1[64:68])
    # checksum1 = int(line1[68])

    catalog2 = alpha5_to_number(line2[2:7])
    i = float(line2[8:16])
    r = float(line2[17:25])
    e = implied_decimal_to_float(line2[26:33])
    p = float(line2[34:42])
    mu = float(line2[43:51])
    n = float(line2[52:63])
    revnum = int(line2[63:68])
    # checksum2 = line2[68]

    if catalog1 != catalog2:
        msg = (
            f"Catalog number for line 1 {catalog1!r} does not match line 2 {catalog2!r}"
        )
        raise ValueError(msg)

    return {
        "classification": classification,
        "catalog": catalog1,
        "intl_des": intl_des,
        "epoch": epoch,
        "n": n,
        "nd": nd,
        "ndd": ndd,
        "bstar": Bstar,
        "type": elset_type,
        "number": element_number,
        "i": i,
        "r": r,
        "e": e,
        "p": p,
        "mu": mu,
        "rev": revnum,
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
    p: float
    """Argument of Perigee (deg)"""
    mu: float
    """Mean Anomaly (deg)"""
    n: float
    """Mean Motion (rev/day)"""
    nd: float
    """Mean Motion 1st Derivative (rev/day^2)"""
    ndd: float
    """Mean Motion 2nd Derivative (rev/day^3)"""
    rev: int
    """Revolution Number at Epoch"""

    @property
    def alpha5(self) -> str:
        """Satellite Catalog Number (Alpha-5 Notation)"""
        return number_to_alpha5(self.catalog)

    @classmethod
    def from_lines(cls, line1: str, line2: str) -> "TLE":
        return cls(**parse_tle(line1, line2))

    def to_lines(self) -> Tuple[str, str]:
        alpha5 = number_to_alpha5(self.catalog)
        epoch = datetime_to_epoch(self.epoch)
        nd = f"{self.nd: .8f}"
        nd = nd[0] + nd[2:]
        ndd = float_to_scinot(self.ndd)
        bstar = float_to_scinot(self.bstar)

        line1 = f"1 {alpha5:5}{self.classification} {self.intl_des} {epoch:14} {nd} {ndd:8} {bstar:8} {self.type} {self.number:4}"
        line1 = line1 + str(compute_checksum(line1))

        e = float_to_implied_decimal(self.e)
        line2 = f"2 {alpha5:5} {self.i:8.4f} {self.r:8.4f} {e:7} {self.p:8.4f} {self.mu:8.4f} {self.n:11.8f}{self.rev:5}"
        line2 = line2 + str(compute_checksum(line2))

        return line1, line2
