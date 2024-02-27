import xmltodict
from pathlib import Path
from trainlocationeventsource.service_layer.services import handle_nstreinpositie
from trainlocationeventsource.domain.nstreinpositie import NStreinpositie
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
        handle_nstreinpositie(parsed, repo=repo)

        treinpositie: NStreinpositie = next(repo)
        assert treinpositie.treinnummer == "8669"
        # assert len(message["trein_materieel_delen"]) == 1
