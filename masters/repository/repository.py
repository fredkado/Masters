from masters.repository.base import AbstractRepository

class SolutionRepository(AbstractRepository):
    
    def __init__(self) -> None:
        from db.models import Solution
        self.solution_model = Solution
    
    def get(self, solution_id):
        return self.solution_model.objects.get(id=solution_id)
    
    def add(self, solution_entity):
        self.solution_model.objects.create(**solution_entity.__dict__)
 
    
class FitnessRepository(AbstractRepository):
    
    def __init__(self) -> None:
        from db.models import Fitness
        self.fitness_model = Fitness
    
    def get(self):
        return
    
    def add(self, solution_id, fitness_value):
        solution = SolutionRepository().get(solution_id)
        self.fitness_model.objects.create(solution=solution, fitness_value=fitness_value)
        
    