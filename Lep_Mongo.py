from mimetypes import init
import pymongo 
from bson.objectid import ObjectId
'''


'''

class Lep_Mongo_Client:
    url = None
    dbname = None
    @staticmethod
    def SetDefaultClientArgs(host:str, port:int, user:str, pswd:str, dbname:str): # mechanism:str='MONGODB-CR'
        Lep_Mongo_Client.host = host
        Lep_Mongo_Client.port = port
        Lep_Mongo_Client.user = user
        Lep_Mongo_Client.pswd = pswd
        Lep_Mongo_Client.dbname = dbname
        # Lep_Mongo_Client.mechanism = mechanism

    def __init__(self, host:str=None, port:int=None, user:str=None, pswd:str=None, dbname:str=None) -> None:    # &authMechanism={self.mechanism}
        self.host       = host if host else Lep_Mongo_Client.host
        self.port       = port if port else Lep_Mongo_Client.port
        self.user       = user if user else Lep_Mongo_Client.user
        self.pswd       = pswd if pswd else Lep_Mongo_Client.pswd
        self.dbname     = dbname if dbname else Lep_Mongo_Client.dbname
        # self.mechanism  = mechanism if mechanism else Lep_Mongo_Client.mechanism
        self.url        = f'mongodb://{self.user}:{self.pswd}@{self.host}:{self.port}/?authSource={self.dbname}'    # &authMechanism={self.mechanism}
        self.client       = pymongo.MongoClient(self.url)
        
        self.db         = self.client[self.dbname]
    
    def get_collections(self)->list:
        '''获取所有集合(表的名称)'''
        return self.db.list_collection_names()

class Lep_Mongo_Collection:
    def __init__(self, coolection_name:str, lepclient:Lep_Mongo_Client=None, session=None):
        self.lepclient = lepclient if lepclient else Lep_Mongo_Client()
        self.session = session
        self.client = self.lepclient.client
        self.db = self.lepclient.db
        self.col = self.db[coolection_name]

    def add(self, data:dict)->str:
        '''添加1条数据, 返回插入的id'''
        return self.col.insert_one(data, session=self.session).inserted_id
    def addmany(self, data:list)->list:
        '''添加多条数据, 返回插入的id列表'''
        return [str(id) for id in self.col.insert_many(data, session=self.session).inserted_ids]

    def getall(self)->list:
        '''获取该集合中所有数据'''
        res = []
        try:
            for item in self.col.find({}, session=self.session):
                res.append(item)
            return res
        except Exception as e:
            res = None
        return res
    def getid(self, id:str)->dict:
        '''从id获取1个document'''
        try:
            return self.col.find_one({'_id': ObjectId(id)}, session=self.session)
        except:
            return None
    def getone(self, query:dict)->dict:
        '''从条件获取1个document'''
        try:
            return self.col.find_one(query, session=self.session)
        except:
            return None
    def get(self, query:dict)->list:
        '''获取符合条件的数据'''
        res = []
        try:
            res = [item for item in self.col.find(query, session=self.session)]
        except Exception as e:
            res = None
        return res
    
    def getlimit(self, query:dict, limit:int)->list:
        '''limit: 限制条数'''
        res = []
        try:
            res = [item for item in self.col.find(query, session=self.session).limit(limit)]
        except Exception as e:
            res = None
        return res

    def getskiplimit(self, query:dict, skip:int, limit:int):
        '''skip: 忽略的个数, limit: 限制的条数'''
        res = []
        try:
            res = [item for item in self.col.find(query, session=self.session).skip(skip).limit(limit)]
        except Exception as e:
            res = None
        return res
    
    def page(self, query:dict, page:int, limit:int):
        res = []
        try:
            res = [item for item in self.col.find(query, session=self.session).skip((page - 1) * limit).limit(limit)]
        except Exception as e:
            res = None
        return res
    



    def count(self, query:dict):
        '''返回collection中符合条件的document数量'''
        return self.col.count_documents(query, session=self.session)
    @property
    def countall(self)->int:
        '''返回collection中document数量'''
        return self.col.count_documents({}, session=self.session)
    
    def objid(self, id)->ObjectId:
        return ObjectId(id)

    def delid(self, id):
        try:
            return self.col.delete_one({'_id': ObjectId(id)}, session=self.session)
        except:
            return None
    def delone(self, query:dict)->int:
        try:
            return self.col.delete_one(query, session=self.session).deleted_count
        except:
            return 0
    def delmany(self, query:dict)->int:
        try:
            return self.col.delete_many(query, session=self.session).deleted_count
        except:
            return 0

    def getonedel(self, query:dict):
        return self.col.find_one_and_delete(query, session=self.session)

    def updateid(self, id, data:dict):
        try:
            res = self.col.update_one({'_id': ObjectId(id)}, {'$set': data}, session=self.session)
            return (res.matched_count, res.modified_count)
        except:
            return None

    def updateone(self, query:dict, data:dict)->int:
        try:
            res = self.col.update_one(query, {'$set': data}, session=self.session)
            return (res.matched_count, res.modified_count)
        except:
            return None

    def updatemany(self, query:dict, data:dict):
        try:
            res = self.col.update_many(query, {'$set': data}, session=self.session)
            return (res.matched_count, res.modified_count)
        except:
            return None

class User(Lep_Mongo_Collection):
    coolection_name = 'user'
    def __init__(self,lepclient:Lep_Mongo_Client=None, session=None): super().__init__(User.coolection_name, lepclient, session)



if __name__ == '__main__':
    Lep_Mongo_Client.SetDefaultClientArgs(host='127.0.0.1', port=27017, user='gfy_admin', pswd='0HliFM7mzwS0wkhA', dbname='guangfuyun')

    # 事务
    # lepclient = Lep_Mongo_Client()
    # with lepclient.client.start_session() as session:
    #     with session.start_transaction():
    #         user = User(lepclient, session)
    #         user.addmany([{'name': '123'}, {'name': '567'}])
    #         ids = user.delmany({})
    #         raise Exception('')        

    user = User()
    id = user.add({'name': 'abc'})
    id = user.add({'name': 'bcd'})
    print(user.page({}, 2, 10))
    








