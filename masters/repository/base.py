from abc import ABCMeta, abstractmethod

class AbstractRepository(metaclass=ABCMeta):
    
    def add(self, *args, **kwargs):
        raise NotImplementedError
    
    def get(self, *args, **kwargs):
        raise NotImplementedError
        