"""Will supply all the services"""

from __future__ import annotations

from trainlocationeventsource.adapters.repository import AbstractRepository
from trainlocationeventsource.domain import NStreinpositie, TreinMaterieelDeel


def handle_nstreinpositie(nstreinpositie: dict, repo: AbstractRepository):
    """Handle a nstreinpositie message. Message must be in a dict format, but still
    adhere to the NStreinpositiesInterface5 standard"""
    treinnummer = nstreinpositie["tns3:ArrayOfTreinLocation"]["tns3:TreinLocation"][
        "tns3:TreinNummer"
    ]
    positie = NStreinpositie(treinnummer=treinnummer, trein_materieel_delen=[])
    result = repo.save(positie)
    return result
    # @TODO Do we need to return anything?
