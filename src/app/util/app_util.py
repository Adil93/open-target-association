def sortRemoveDuplicateAndGetTopthree(rowList):
    res = list(dict.fromkeys(rowList))
    res.sort(reverse=True)
    return res[:3]
