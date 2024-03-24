from __future__ import annotations

import abc
import datetime
import json
import logging

import attrs
from esdbclient import EventStoreDBClient, NewEvent, StreamState

from trainlocationeventsource.domain import NStreinpositie

logger = logging.getLogger(__name__)


class AbstractRepository(abc.ABC):
    """Repository that will be used to store and retrieve the Domain to the database"""

    @abc.abstractmethod
    def save(self, posities: list[NStreinpositie]):
        # As for naming, maybe `save`?
        # esdbclient calls it `append_to_stream`. But the question is, are we going to
        # use esdb? And, do we want to have the terminology of the database structure
        # exposed here, or are we abstracting this detail away?
        # Maybe an even better name is `save_update`, since we are saving a position
        # update. Or `save_treinpositie`, since this makes what we are saving explicit.
        #
        # There are 2 hard problems in computer science:
        # cache invalidation, naming things, and off-by-1 errors.
        raise NotImplementedError


def serialize(inst, field, value):
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


class EventStoreDBRepository(AbstractRepository):
    """Store the domain to the EvenstoreDB"""

    def __init__(self, client: EventStoreDBClient):
        self.client = client

    @staticmethod
    def compute_streamname(positie: NStreinpositie):
        return f"NStreinpositie.{positie.treinnummer}"

    def save(self, posities: list[NStreinpositie]):
        for positie in posities:
            self._stream_record(positie)

    def _stream_record(self, positie: NStreinpositie):
        """Save new records to the EvenstoreDB."""
        # @TODO The repository here has knowledge about how to serialize data to json
        #    should this functionality be here?
        data = attrs.asdict(positie, value_serializer=serialize)
        event = NewEvent(
            # id=uuid.uuid4(),
            type="NStreinpositie",
            data=json.dumps(data).encode("utf8"),
        )
        self.client.append_to_stream(
            stream_name=self.compute_streamname(positie),
            events=[event],
            current_version=StreamState.ANY,
        )
