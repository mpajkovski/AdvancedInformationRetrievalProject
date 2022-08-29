def base_judgment(df):
    j = stats.mode(df['RelevanceScore'])
    if j[1][0]!=1:
        return j[0][0]
    else:
        return max(df['RelevanceScore'])
    
def judgment(df):
    j = stats.mode(df['CenteredRelevanceScore'])
    if j[1][0]!=1:
        z = int(j[0][0] -find_disagreement(df.CenteredRelevanceScore.values))
        if z==0:
            return 1
        return z
    else:
        z = int((df.CenteredRelevanceScore.mean()- find_disagreement(df.CenteredRelevanceScore.values)))
        if z==0:
            return 1
        return z
    
def find_disagreement(j):
    if len(j)==1:
        return 0
    elif len(j)==2:
        return np.abs(j[0]-j[1])/2
    else:
        return (np.abs(j[0]-j[1])/2 + np.abs(j[0]-j[2])/2 + np.abs(j[1]-j[1])/2)/3