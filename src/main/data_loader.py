from util.app_util import sortRemoveDuplicateAndGetTopthree
from util.ftp_loader import FtpLoader
from service.open_target_service import getResultantAssociationScoreMedianData
import pandas as pd

FTP_HOST = "ftp.ebi.ac.uk"
EVIDENCE_DIR_NAME = "/pub/databases/opentargets/platform/21.11/output/etl/json/evidence/sourceId=eva/"
TARGET_DIR_NAME = "/pub/databases/opentargets/platform/21.11/output/etl/json/targets/"
DISEASE_DIR_NAME = "/pub/databases/opentargets/platform/21.11/output/etl/json/diseases/"

ftpLoader = FtpLoader(FTP_HOST)

evidenceData = pd.DataFrame(ftpLoader.loadData(EVIDENCE_DIR_NAME, "evidence"))
targetData = pd.DataFrame(ftpLoader.loadData(TARGET_DIR_NAME, "target"))
diseaseData = pd.DataFrame(ftpLoader.loadData(DISEASE_DIR_NAME, "disease"))

resultantData = getResultantAssociationScoreMedianData(
    evidenceData, targetData, diseaseData)

resultantData.to_json('data/result.json', orient='records')

targetCountWithMoreThan1DiseaseRelation = resultantData.groupby(
    'targetId')['targetId'].filter(lambda x: len(x) > 1).count()

targetPairCount = targetCountWithMoreThan1DiseaseRelation * (
    targetCountWithMoreThan1DiseaseRelation-1)/2

print("Number of targets having relation with more than one disease : {0} ".format(
    targetCountWithMoreThan1DiseaseRelation))
print("Number of unique target pairs having relation with more than one disease : {0} ".format(
    targetPairCount))

print(resultantData)
