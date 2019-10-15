from db import ConnectDb
from db.sql.InsertFaceFeaturesSql import *


class InertFaceFeatures:
    server = "10.1.32.104:34111"
    user = "cdd_test"
    password = "hQyfzpRHN2nuuj89"
    database = "test"

    def __init__(self):
        self.mssql = ConnectDb.MSSQL(self.server, self.user, self.password, self.database)

    def insert(self, name, faceFeatures):
        try:
            # 查找是否已有特征数据
            rows = self.mssql.ExecQuery(selectFaceCount(name))
            if len(rows) > 0:
                self.mssql.ExecNonQuery(updateFace(name,faceFeatures))
            else:
                self.mssql.ExecNonQuery(insertFace(name,faceFeatures) )

        except Exception as ex:
            self.mssql.rollback()
            raise ex
        finally:
            self.mssql.close()

if __name__ == '__main__':
    iff = InertFaceFeatures()
    iff.insert('sxf','dasfdsa')
