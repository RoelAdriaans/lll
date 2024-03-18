from __future__ import annotations

import abc

from esdbclient import EventStoreDBClient

from trainlocationeventsource.adapters.repository import (
    AbstractRepository,
    EventStoreDBRepository,
)


class AbstractUnitOfWork(abc.ABC):
    posities: AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
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
