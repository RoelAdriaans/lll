from pathlib import Path

import pytest
import xmltodict

from trainlocationeventsource.domain.nstreinpositie import NStreinpositie
from trainlocationeventsource.service_layer.services import handle_nstreinpositie

from .fakeunitofwork import FakeUnitOfWork


class TestNstreinpositie:
    def _read_data_file(self, filename: str) -> str:
        """Open a file and return the raw XML data"""
        # Read the message
        with open(Path(__file__).parent / "nstreinpositiedata" / filename) as f:
            return f.read()

    @pytest.mark.parametrize(
        ("filename", "nr_treinlocation", "nr_treinmaterieeldelen"),
        [
            pytest.param("multiple_messages.xml", 2, 3, id="multiple_messages.xml"),
            pytest.param("dual_treindeel.xml", 1, 2, id="dual_treindeel.xml"),
            pytest.param("single_message.xml", 1, 1, id="single_message.xml"),
            pytest.param("empty_message.xml", 0, 0, id="empty_message.xml"),
        ],
    )
    def test_message_counts(
        self, filename: str, nr_treinlocation: int, nr_treinmaterieeldelen: int
    ):
        # Arrange
        xml_message = self._read_data_file(filename)
        parsed = xmltodict.parse(xml_message)
        uow = FakeUnitOfWork()

        # Act
        handle_nstreinpositie(parsed, uow=uow)
        treinlocations = len(uow.posities)
        trein_delen = sum([len(pos.trein_materieel_delen) for pos in uow.posities])

        # Assert
        assert uow.committed
        assert treinlocations == nr_treinlocation
        assert trein_delen == nr_treinmaterieeldelen

    def test_single_message(self):
        # Arrange
        xml_message = self._read_data_file("single_message.xml")
        parsed = xmltodict.parse(xml_message)
        uow = FakeUnitOfWork()

        # Act
        handle_nstreinpositie(parsed, uow=uow)
        treinpositie: NStreinpositie = uow.posities[0]
        deel1 = treinpositie.trein_materieel_delen[0]

        # Assert
        assert isinstance(treinpositie, NStreinpositie)
        assert treinpositie.treinnummer == "8669"
        assert len(treinpositie.trein_materieel_delen) == 1
        assert deel1.materieel_deel_nummer == "2010"
        assert deel1.materieelvolgnummer == 1

    def test_multiple_messages(self):
        # Arrange
        xml_message = self._read_data_file("multiple_messages.xml")
        parsed = xmltodict.parse(xml_message)
        uow = FakeUnitOfWork()

        # Act
        handle_nstreinpositie(parsed, uow=uow)
        assert len(uow.posities) == 2

        treinpositie: NStreinpositie = uow.posities[0]
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
        uow = FakeUnitOfWork()

        # Act
        handle_nstreinpositie(parsed, uow=uow)
        treinpositie: NStreinpositie = uow.posities[0]
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
