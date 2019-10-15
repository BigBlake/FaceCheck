def selectFaceCount(name):
    sql = 'SELECT UserId FROM test.dbo.FaceFeatures ff ' \
          'INNER JOIN test.dbo.UserInfo ui ON ui.id = ff.UserId ' \
          'WHERE ui.Name = \'' + name + '\''
    print(sql)
    return sql


def insertFace(name, faceFeatures):
    sql = 'INSERT INTO test.dbo.FaceFeatures  (UserId, Features) \
            SELECT id,\'' + faceFeatures + '\' FROM test.dbo.UserInfo WHERE Name = \'' + name + '\''
    print(sql)
    return sql


def updateFace(name, faceFeatures):
    sql = 'UPDATE ff SET ff.Features = \'' + faceFeatures + '\' ,updatetime = getdate() \
            FROM test.dbo.FaceFeatures ff \
            INNER JOIN test.dbo.UserInfo ui ON ui.id = ff.UserId \
            WHERE ui.Name = \'' + name + '\''
    print(sql)
    return sql
