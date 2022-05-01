from util import logger_util
from util.ftp_loader import FtpLoader
from service.open_target_service import getResultantAssociationScoreMedianData, getTargetCountHavingMoreThanOneDiseaseRelation, getTargetPairsCountHavingMoreThanOneDiseaseRelation
import concurrent.futures
import time
import pandas as pd
import logging as logger
import os


logger_util.setup()

FTP_HOST = "ftp.ebi.ac.uk"
EVIDENCE_DIR_NAME = "/pub/databases/opentargets/platform/21.11/output/etl/json/evidence/sourceId=eva/"
TARGET_DIR_NAME = "/pub/databases/opentargets/platform/21.11/output/etl/json/targets/"
DISEASE_DIR_NAME = "/pub/databases/opentargets/platform/21.11/output/etl/json/diseases/"


ftpLoader = FtpLoader(FTP_HOST)

evidenceData = pd.DataFrame()
targetData = pd.DataFrame()
diseaseData = pd.DataFrame()


os.chdir("data/")
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    logger.info("Starting Concurrent Data loading")
    evidenceFuture = executor.submit(
        ftpLoader.loadData, EVIDENCE_DIR_NAME, "evidence")
    targetFuture = executor.submit(
        ftpLoader.loadData, TARGET_DIR_NAME, "target")
    diseaseFuture = executor.submit(
        ftpLoader.loadData, DISEASE_DIR_NAME, "disease")

    while not (evidenceFuture.done() and targetFuture.done() and diseaseFuture.done):
        logger.info("Evidence Fetch Completed: {0} -- Target Fetch Completed: {1} -- Disease Fetch Completed: {2}".format(
            evidenceFuture.done(), targetFuture.done(), diseaseFuture.done()))
        logger.info("Waiting 10 seconds..........")
        time.sleep(10)
    evidenceData = pd.DataFrame(evidenceFuture.result())
    targetData = pd.DataFrame(targetFuture.result())
    diseaseData = pd.DataFrame(diseaseFuture.result())

logger.info("Successfully fetched all data")

resulData = getResultantAssociationScoreMedianData(
    evidenceData, targetData, diseaseData)

resulData.to_json('result.json', orient='records')

targetCountWithMoreThan1DiseaseRelation = getTargetCountHavingMoreThanOneDiseaseRelation(
    resulData)

targetPairCount = getTargetPairsCountHavingMoreThanOneDiseaseRelation(
    resulData)

logger.info("Number of targets having relation with more than one disease : {0} ".format(
    targetCountWithMoreThan1DiseaseRelation))
logger.info("Number of unique target pairs having relation with more than one disease : {0} ".format(
    targetPairCount))

logger.info("\n %s", resulData)
