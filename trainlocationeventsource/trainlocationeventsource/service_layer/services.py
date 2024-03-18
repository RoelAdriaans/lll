"""Will supply all the services"""

from __future__ import annotations

from datetime import datetime

from trainlocationeventsource.domain import NStreinpositie, TreinMaterieelDeel
from trainlocationeventsource.service_layer import unit_of_work


def handle_nstreinpositie(nstreinpositie: dict, uow: unit_of_work.AbstractUnitOfWork):
    """Handle a nstreinpositie message. Message must be in a dict format, but still
    adhere to the NStreinpositiesInterface5 standard.
    Saves the new Treinpositie in the repository"""
    delen = _parse_treinmaterieeldelen(nstreinpositie)
    positie = _parse_nstreinpositie(nstreinpositie, trein_materieel_delen=delen)
    with uow:
        uow.posities.save(positie)


def _parse_treinmaterieeldelen(nstreinpositie: dict) -> list[TreinMaterieelDeel]:
    print("Pos")
    print(nstreinpositie)
    delen = nstreinpositie["tns3:ArrayOfTreinLocation"]["tns3:TreinLocation"][
        "tns:TreinMaterieelDelen"
    ]
    if isinstance(delen, list):
        return [_parse_treinmaterieeldeel(deel) for deel in delen]
    else:
        return [_parse_treinmaterieeldeel(delen)]


def _parse_treinmaterieeldeel(treinmaterieeldeel: dict) -> TreinMaterieelDeel:
    """Parse a single instance of the treinmaterieeldeel dict"""
    tmd = TreinMaterieelDeel(
        materieel_deel_nummer=treinmaterieeldeel["tns:MaterieelDeelNummer"],
        materieelvolgnummer=int(treinmaterieeldeel["tns:Materieelvolgnummer"]),
        generatie_tijd=treinmaterieeldeel["tns:GeneratieTijd"],
        gps_datumtijd=datetime.fromisoformat(treinmaterieeldeel["tns:GpsDatumTijd"]),
        orientatie=treinmaterieeldeel["tns:Orientatie"],
        bronid=treinmaterieeldeel["tns:BronId"],
        bron=treinmaterieeldeel["tns:Bron"],
        fix=(
            int(treinmaterieeldeel["tns:Fix"])
            if treinmaterieeldeel["tns:Fix"]
            else None
        ),
        berichttype=treinmaterieeldeel["tns:Berichttype"],
        longitude=float(treinmaterieeldeel["tns:Longitude"]),
        latitude=float(treinmaterieeldeel["tns:Latitude"]),
        elevation=float(treinmaterieeldeel["tns:Elevation"]),
        snelheid=float(treinmaterieeldeel["tns:Snelheid"]),
        richting=treinmaterieeldeel["tns:Richting"],
        rijrichting=treinmaterieeldeel["tns:Rijrichting"],
        hdop=float(treinmaterieeldeel["tns:Hdop"]),
        aantal_satelieten=int(treinmaterieeldeel["tns:AantalSatelieten"]),
    )

    return tmd


def _parse_nstreinpositie(
    nstreinpositie: dict, trein_materieel_delen: list[TreinMaterieelDeel]
) -> NStreinpositie:
    """Parse a nstreinpositie"""
    treinnummer = nstreinpositie["tns3:ArrayOfTreinLocation"]["tns3:TreinLocation"][
        "tns3:TreinNummer"
    ]
    return NStreinpositie(
        treinnummer=treinnummer, trein_materieel_delen=trein_materieel_delen
    )
