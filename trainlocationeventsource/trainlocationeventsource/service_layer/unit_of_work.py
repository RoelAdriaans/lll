from __future__ import annotations

import abc
import datetime
import logging

from esdbclient import EventStoreDBClient

from trainlocationeventsource.adapters.repository import (
    AbstractRepository,
    EventStoreDBRepository,
)

logger = logging.getLogger(__name__)


class AbstractUnitOfWork(abc.ABC):
    posities: AbstractRepository
    start_time: datetime.datetime

    def __enter__(self) -> AbstractUnitOfWork:
        self.start_time = datetime.datetime.now()
        return self

    def __exit__(self, *args):
        end_time = datetime.datetime.now()
        logger.info("Saving events took %s seconds", end_time - self.start_time)
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class EventstoreDBUnitOfWork(AbstractUnitOfWork):
    def __init__(self): ...

    def __enter__(self):
        # @TODO Make the hostname configurable / Detect from env.vars
        self.client = EventStoreDBClient(uri="esdb://localhost:2113?Tls=false")
        self.posities = EventStoreDBRepository(self.client)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.client.close()

    def commit(self):
        ...
        # EventStoreDB does not have a commit?

    def rollback(self):
        ...
        # EventStoreDB does not have a rollback?
