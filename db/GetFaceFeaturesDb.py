from db import ConnectDb
from db.sql.GetFaceFeaturesSql import getFace
from db.sql.InsertFaceFeaturesSql import *


class GetFaceFeaturesDb:
    server = "10.1.32.104:34111"
    user = "cdd_test"
    password = "hQyfzpRHN2nuuj89"
    database = "test"

    def __init__(self):
        self.mssql = ConnectDb.MSSQL(self.server, self.user, self.password, self.database)

    def getFace(self):
        try:
            rows = self.mssql.ExecQuery(getFace())
            return rows
        except Exception as ex:
            self.mssql.rollback()
            raise ex
        finally:
            self.mssql.close()

if __name__ == '__main__':
    iff = GetFaceFeaturesDb()
    iff.getFace()
