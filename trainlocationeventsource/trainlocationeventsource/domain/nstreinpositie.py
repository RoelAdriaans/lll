"""Convert messages from the NStreinpositiesInterface5 endpoint into a usable dict

XML Spec defines thinks like TreinNummer, but this is not a pythonesque naming schema.
XML entities are changes to be more Pythonic, eg lowercase and separated by underscores.
TreinNummer will thus be renamed to trein_nummer.
"""

from __future__ import annotations

from datetime import date, datetime

import attrs


@attrs.define(frozen=True)
class NStreinpositie:
    """Trein Positie"""

    treinnummer: str
    trein_materieel_delen: list[TreinMaterieelDeel]


@attrs.define(frozen=True)
class TreinMaterieelDeel:
    """Materiaaldeel"""

    materieel_deel_nummer: str
    materieelvolgnummer: int
    # Unixtimestamp. Always null?
    generatie_tijd: int | None
    gps_datumtijd: datetime
    # This should be the travel oriantation. Spec says that the data is unreliable
    # and not to use it.
    orientatie: float | None
    bronid: None
    bron: str
    # GPS Fix? 1 = Fix, 0 = no fix
    fix: int
    # Actuele Materieelpositie?
    berichttype: None
    # GPS Coordinates
    longitude: float
    latitude: float
    elevation: float
    snelheid: float
    richting: float
    # Currently not stable or provided
    rijrichting: None
    # Horizontale dilution of position.
    hdop: float
    aantal_satelieten: int
