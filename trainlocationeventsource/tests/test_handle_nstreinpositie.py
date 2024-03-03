from pathlib import Path

import xmltodict

from trainlocationeventsource.domain.nstreinpositie import NStreinpositie
from trainlocationeventsource.service_layer.services import handle_nstreinpositie

from .fakerepository import FakeRepository


class TestNstreinpositie:
    def _read_data_file(self, filename: str) -> str:
        """Open a file and return the raw XML data"""
        # Read the message
        with open(Path(__file__).parent / "nstreinpositiedata" / filename) as f:
            return f.read()

    def test_single_message(self):
        # Arrange
        xml_message = self._read_data_file("single_message.xml")
        parsed = xmltodict.parse(xml_message)
        repo = FakeRepository()

        # Act
        handle_nstreinpositie(parsed, repository=repo)
        treinpositie: NStreinpositie = next(repo)
        deel1 = treinpositie.trein_materieel_delen[0]

        # Assert
        assert isinstance(treinpositie, NStreinpositie)
        assert treinpositie.treinnummer == "8669"
        assert len(treinpositie.trein_materieel_delen) == 1
        assert deel1.materieel_deel_nummer == "2010"
        assert deel1.materieelvolgnummer == 1

    def test_dual_treindeele(self):
        # Arrange
        xml_message = self._read_data_file("dual_treindeel.xml")
        parsed = xmltodict.parse(xml_message)
        repo = FakeRepository()

        # Act
        handle_nstreinpositie(parsed, repository=repo)
        treinpositie: NStreinpositie = next(repo)
        deel1 = treinpositie.trein_materieel_delen[0]
        deel2 = treinpositie.trein_materieel_delen[1]

        # Assert
        assert isinstance(treinpositie, NStreinpositie)
        assert treinpositie.treinnummer == "6624"
        assert len(treinpositie.trein_materieel_delen) == 2
        assert deel1.materieel_deel_nummer == "2508"
        assert deel1.materieelvolgnummer == 1
        assert deel2.materieel_deel_nummer == "2205"
        assert deel2.materieelvolgnummer == 2
