def getFace():
    sql = 'SELECT f.UserId,u.Name,f.Features FROM test.dbo.UserInfo u \
            INNER JOIN test.dbo.FaceFeatures f ON u.id = f.UserId'
    print(sql)
    return sql

