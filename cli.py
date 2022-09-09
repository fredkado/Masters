import typer
from masters.usecases.usecases import add_solution, add_fitness
from masters.usecases.usecases import run_ga
from masters.repository.repository import SolutionRepository, FitnessRepository
from masters.repository.garepository import GeneticAlgorithmRepository, fitness, varbound
import ast

app = typer.Typer()

@app.command()
def simulate_add_solution(solution_info):
    add_solution(SolutionRepository, {'chromosone':ast.literal_eval(solution_info)})
    
@app.command()
def simulate_add_fitness(solution_id, fitness_value):
    add_fitness(FitnessRepository, solution_id, fitness_value)

@app.command()
def test_run_ga(dimension:int=typer.Option(prompt=True, default=88),
                variable_type:str=typer.Option(prompt=True, default='int'),
                function_timeout:float=typer.Option(prompt=True, default=30.0),
                
                max_num_iteration:int=typer.Option(prompt=True, default=100),
                population_size:int=typer.Option(prompt=True, default=100),
                mutation_probability:float=typer.Option(prompt=True, default=0.1),
                elit_ratio:float=typer.Option(prompt=True, default=0.01),
                crossover_probability:float=typer.Option(prompt=True, default=0.5),
                parents_portion:float=typer.Option(prompt=True, default=0.3),
                crossover_type:str=typer.Option(prompt=True, default='uniform'),
                max_iteration_without_improv:int=typer.Option(prompt=True, default=None)):
    
    algorithm_params = dict(
        max_num_iteration=max_num_iteration, population_size=population_size,
        mutation_probability=mutation_probability, elit_ratio=elit_ratio,
        crossover_probability=crossover_probability, parents_portion=parents_portion,
        crossover_type=crossover_type, max_iteration_without_improv=max_iteration_without_improv
    )
    
    print('Running GA')
    
    run_ga(GeneticAlgorithmRepository, fitness, dimension, variable_type, varbound, function_timeout, algorithm_params)

if __name__ == '__main__':
    app()

