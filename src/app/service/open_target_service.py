import pandas as pd
import logging as logger


from app.util.app_util import sortRemoveDuplicateAndGetTopthree


def getResultantAssociationScoreMedianData(evidenceData=pd.DataFrame(), targetData=pd.DataFrame(), diseaseData=pd.DataFrame()):
    logger.info("Begin getResultantAssociationScoreMedianData")
    topThreeScoreData = evidenceData.sort_values('score', ascending=False).groupby(
        ['targetId', 'diseaseId'])['score'].apply(list).reset_index(name="topThreeScores")
    topThreeScoreData['topThreeScores'] = topThreeScoreData['topThreeScores'].apply(
        lambda row:
            sortRemoveDuplicateAndGetTopthree(row)
    )

    medianData = evidenceData.groupby(['targetId', 'diseaseId'])[
        'score'].median().reset_index(name="median")

    medianWithTopThreeData = topThreeScoreData.merge(
        medianData, how='left', on=['targetId', 'diseaseId'])

    medianWithTopThreeData = medianWithTopThreeData.sort_values(by='median')

    targetResultData = medianWithTopThreeData.merge(
        targetData, how='left', left_on='targetId', right_on='id')

    diseaseResultData = targetResultData.merge(
        diseaseData, how='left', left_on='diseaseId', right_on='id'
    )

    resultData = diseaseResultData[[
        'targetId', 'approvedSymbol', 'diseaseId', 'name', 'topThreeScores', 'median']]
    logger.info("End getResultantAssociationScoreMedianData")
    return resultData


def getTargetCountHavingMoreThanOneDiseaseRelation(resultData=pd.DataFrame()):
    return resultData.groupby(
        'targetId')['targetId'].filter(lambda x: len(x) > 1).count()


def getTargetPairsCountHavingMoreThanOneDiseaseRelation(resultData=pd.DataFrame()):
    targetCount = getTargetCountHavingMoreThanOneDiseaseRelation(resultData)
    return targetCount * (targetCount-1)/2
