import os
from src.logger import my_logger
from src.utils import increment_path, load_config, create_yaml
from src.data_generation import create_data
from src.plotting import plot_comparison_graphs
from src.execution import execute_algorithm


# Change only this
yaml_name = "exp6_CustomerChurn.yaml"

config_path = "configs/"  # Folder to load config file
# Configuration
config = load_config(yaml_name, config_path)
show_graphs = config.get('show_graphs')
perform_test = config.get('perform_test')

# Save path
base_path = 'runs/'
experiment_path = os.path.join(base_path, os.path.splitext(yaml_name)[0])
# if there is an experiment with same experiment.yaml, increment_path_number exp1, exp2....
incremented_path = increment_path(experiment_path, exist_ok=False, sep='_', mkdir=True)
print(f"Results will be saved to: {incremented_path}")

# Create logger
logging = my_logger(incremented_path)

if __name__ == '__main__':

    # Create Data
    logging.info("Creating data points")
    A, test_data = create_data(config.get('data'))
    n, m = A.shape

    # Start Algorithms
    results = {}
    solver_methods = config.get('solver_methods')
    for method in solver_methods:
        train, test = execute_algorithm(method, A, config, incremented_path, test_data)
        results[method] = (train, test)

    show_graphs = config.get('show_graphs')
    graph_path = os.path.join(incremented_path)
    plot_comparison_graphs(results, show_graphs, graph_path)

    if perform_test:
        test_size = len(test_data[1])
    else:
        test_size = 0

    # Create yaml content
    create_yaml(m, test_size, config, incremented_path, results)
