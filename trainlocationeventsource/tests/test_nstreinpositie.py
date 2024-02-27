from trainlocationeventsource.domain.nstreinpositie import NStreinpositie, TreinMaterieelDeel


class TestNstreinpositie:
    def _read_data_file(self, filename: str) -> str:
        """Open a file and return the raw XML data"""
        # Read the message
        with open(f"nstreinpositiedata/{filename}") as f:
            return f.read()

    def test_single_message(self):
        # Arrange
        xml_message = self._read_data_file("single_message.xml")

        position = NStreinpositie.from_xml(xml_message)

        assert len(position) == 1
        assert len(position[0].trein_materieel_delen) == 1
        treinlocation: TreinMaterieelDeel = position[0].trein_materieel_delen[0]
        assert treinlocation.bron == "GNSS1"
