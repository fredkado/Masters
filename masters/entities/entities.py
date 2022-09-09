from pydantic import BaseModel, validator
from typing import List

class Solution(BaseModel):
    chromosone: List[int]
    
    @validator('chromosone')
    def check_chromosone(cls, val):
        assert len(val) <= 88, 'Invalid solution size'
        return val
    
    def __dict__(self):
        return {'chromosone':self.chromosone}

class Fitness(BaseModel):
    solution: Solution
    fitness_value: float
    
    
    
    