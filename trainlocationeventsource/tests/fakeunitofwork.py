from trainlocationeventsource.service_layer import unit_of_work

from .fakerepository import FakeRepository


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.posities = FakeRepository()
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
