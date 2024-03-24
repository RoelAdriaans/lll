from trainlocationeventsource.adapters import repository
from trainlocationeventsource.domain import NStreinpositie


class FakeRepository(repository.AbstractRepository):
    def __init__(self):
        self._positions = []
        self._index = 0

    def save(self, posities: list[NStreinpositie]):
        for positie in posities:
            self._positions.append(positie)

    def __len__(self) -> int:
        return len(self._positions)

    def __iter__(self):
        yield from self._positions

    def __getitem__(self, item):
        return self._positions[item]

    def get(self, index: int) -> NStreinpositie:
        return self._positions[index]
