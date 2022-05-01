import unittest
import pandas as pd

from app.service.open_target_service import getResultantAssociationScoreMedianData


class TestOpenTargetService(unittest.TestCase):

    def test_get_result(self):
        dataStr = open("resource/test/evidenceData.json", "r").read()
        evidenceData = pd.read_json(dataStr, lines=True)

        dataStr = open("resource/test/targetData.json", "r").read()
        targetData = pd.read_json(dataStr, lines=True)

        dataStr = open("resource/test/diseaseData.json", "r").read()
        diseaseData = pd.read_json(dataStr, lines=True)

        resultData = getResultantAssociationScoreMedianData(
            evidenceData, targetData, diseaseData)

        self.assertEquals(len(resultData.index), 8)


if __name__ == '__main__':
    unittest.main()
