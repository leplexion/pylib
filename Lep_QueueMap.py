from queue import Queue
from .lep_time import get_now_origin
import copy

class LEPQUEUE_ERROR(Exception): pass

class Lep_QueueMap:
    map = {}
    def __init__(self, ownername:str, owner) -> None:
        setattr(owner, 'qmap', self)
        self.owner = owner
        self.ownername:str = ownername
        
    def exist_name_check(self, name):
        if Lep_QueueMap.map.__contains__(name): raise LEPQUEUE_ERROR(f'队列中已存在此命名{name}')

    def not_exist_name_check(self, name):
        if not Lep_QueueMap.map.__contains__(name): raise LEPQUEUE_ERROR(f'队列中不存在此命名{name}')

    def add(self, name:str, maxsize:int = 0):
        self.exist_name_check(name)
        Lep_QueueMap.map[name] =  Queue(maxsize)
    
    def putfn(self, name:str, fnname: str, usercopy:bool = False, *para_list, **para_dict):
        self.not_exist_name_check(name)
        if usercopy:
            copy_para_list = copy.deepcopy(para_list)
            copy_para_dict = copy.deepcopy(para_dict)
        else:
            copy_para_list = para_list
            copy_para_dict = para_dict
        Lep_QueueMap.map[name].put({'fnname':fnname, 'para_list': copy_para_list, 'para_dict': copy_para_dict, 'time': get_now_origin()})

    def getfnall(self):
        self.not_exist_name_check(self.ownername)
        q:Queue = Lep_QueueMap.map[self.ownername]
        while not q.empty():
            act:dict = q.get()
            fn = getattr(self.owner, act['fnname'], None) 
            fn(*act['para_list'], **act['para_dict'])

    
        
