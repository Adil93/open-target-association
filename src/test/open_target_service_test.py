import unittest
import pandas as pd

from app.service.open_target_service import getResultantAssociationScoreMedianData, getTargetCountHavingMoreThanOneDiseaseRelation

# Load test data
dataStr = open("resource/test/evidenceData.json", "r").read()
evidenceData = pd.read_json(dataStr, lines=True)

dataStr = open("resource/test/targetData.json", "r").read()
targetData = pd.read_json(dataStr, lines=True)

dataStr = open("resource/test/diseaseData.json", "r").read()
diseaseData = pd.read_json(dataStr, lines=True)


class TestOpenTargetService(unittest.TestCase):

    def test_get_resultant_data_from_evidence_target_disease_data(self):
        print(
            "\nRUN: test_get_resultant_data_from_evidence_target_disease_data")

        resultData = getResultantAssociationScoreMedianData(
            evidenceData, targetData, diseaseData)

        self.assertEquals(len(resultData.index), 8)

    def test_get_target_pair_count_with_more_than_one_disease_relation(self):
        print(
            "\nRUN: test_get_target_pair_count_with_more_than_one_disease_relation")
        resultData = getResultantAssociationScoreMedianData(
            evidenceData, targetData, diseaseData)
        count = getTargetCountHavingMoreThanOneDiseaseRelation(resultData)
        self.assertEquals(count, 7)


if __name__ == '__main__':
    unittest.main()
