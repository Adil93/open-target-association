import pandas as pd

from util.app_util import sortRemoveDuplicateAndGetTopthree


def getResultantAssociationScoreMedianData(evidenceData=pd.DataFrame(), targetData=pd.DataFrame(), diseaseData=pd.DataFrame()):
    topThreeScoreData = evidenceData.sort_values('score', ascending=False).groupby(
        ['targetId', 'diseaseId'])['score'].apply(list).reset_index(name="topThreeScores")
    topThreeScoreData['topThreeScores'] = topThreeScoreData['topThreeScores'].apply(
        lambda row:
            sortRemoveDuplicateAndGetTopthree(row)
    )

    medianData = evidenceData.groupby(['targetId', 'diseaseId'])[
        'score'].median().reset_index(name="median")

    resultData = topThreeScoreData.merge(
        medianData, how='left', on=['targetId', 'diseaseId'])

    resultData = resultData.sort_values(by='median')

    targetResultData = resultData.merge(
        targetData, how='left', left_on='targetId', right_on='id')

    diseaseResultData = targetResultData.merge(
        diseaseData, how='left', left_on='diseaseId', right_on='id'
    )

    resultantData = diseaseResultData[[
        'targetId', 'approvedSymbol', 'diseaseId', 'name', 'topThreeScores', 'median']]
    return resultantData
