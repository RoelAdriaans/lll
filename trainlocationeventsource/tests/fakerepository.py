from trainlocationeventsource.adapters import repository
from trainlocationeventsource.domain import NStreinpositie


class FakeRepository(repository.AbstractRepository):
    def __init__(self):
        self._positions = []
        self._index = 0

    def save(self, positie: NStreinpositie):
        self._positions.append(positie)

    def __iter__(self):
        return self

    def __next__(self):
        while self._index < len(self._positions):
            return self._positions[self._index]
        raise StopIteration

    def get(self, index: int) -> NStreinpositie:
        return self._positions[index]
