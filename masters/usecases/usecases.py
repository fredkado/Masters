from masters.entities.entities import Solution

def add_solution(repo, solution_info:dict):
    solution = Solution(**solution_info)
    repo().add(solution)
    
def add_fitness(repo, solution_id:int, fitness_value:float):
    repo().add(solution_id, fitness_value)
    

def run_ga(ga_repo,  fitness, dimension, variable_type, varbound, function_timeout, algorithm_params):
    ga_repo(function=fitness, dimension=dimension,
            variable_type=variable_type, variable_boundaries=varbound,
            function_timeout=function_timeout,
            algorithm_parameters=algorithm_params).run()
        
    
        
        
    
    