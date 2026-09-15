import itertools
import mlflow
import numpy as np
import yaml
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

# Load parameters from configuration file
with open("/home/msis/ahegde/aml-lab/projects/notebooks/config.yaml", "r") as f:
  config = yaml.safe_load(f)

linspace_configs = config["linspace_configs"]
test_sizes = config["dataset"]["test_sizes"]
random_state = config["dataset"]["random_state"]
noise_mean = config["dataset"]["noise_mean"]
stddev = config["dataset"]["stddev"]
degrees = config["model"]["degrees"]

experiment_name = "Polynomial_Regression_Grid_Search"
mlflow.set_experiment(experiment_name)
experiment = mlflow.get_experiment_by_name(experiment_name)

# Grid Search Iteration over all parameter combinations
for ls_cfg, test_size in itertools.product(linspace_configs, test_sizes):
  start, stop, num = ls_cfg["start"], ls_cfg["stop"], ls_cfg["num"]

  # Generate dataset per linspace configuration[cite: 2]
  np.random.seed(random_state)
  x = np.linspace(start, stop, num).reshape(-1, 1)
  y = 2 + 0.5 * x[:, 0] ** 2 + np.random.normal(noise_mean, stddev, num)

  # Split dataset[cite: 2]
  x_train, x_test, y_train, y_test = train_test_split(
      x, y, test_size=test_size, random_state=random_state
  )

  for degree in degrees:
    # Build MLflow filter string to avoid duplicate runs
    filter_string = (
        f"params.degree = '{degree}' AND "
        f"params.test_size = '{test_size}' AND "
        f"params.linspace_start = '{start}' AND "
        f"params.linspace_stop = '{stop}' AND "
        f"params.linspace_num = '{num}' AND "
        f"params.random_state = '{random_state}' AND "
        f"params.stddev = '{stddev}'"
    )

    existing_runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id], filter_string=filter_string
    )

    if not existing_runs.empty:
      print(
          f"Skipping: degree={degree}, test_size={test_size},"
          f" linspace=({start}, {stop}, {num}) (Run already exists)"
      )
      continue

    run_name = f"deg_{degree}_ts_{test_size}_ls_{start}_{stop}_{num}"
    with mlflow.start_run(run_name=run_name):
      # Fit model pipeline[cite: 2]
      model = make_pipeline(
          PolynomialFeatures(degree=degree, include_bias=False),
          LinearRegression(),
      )
      model.fit(x_train, y_train)

      # Predict and compute metrics[cite: 2]
      train_pred = model.predict(x_train)
      test_pred = model.predict(x_test)

      train_mse = mean_squared_error(y_train, train_pred)
      test_mse = mean_squared_error(y_test, test_pred)
      mse_diff = test_mse - train_mse
      mse_ratio = test_mse / train_mse if train_mse != 0 else np.nan

      # Log parameters[cite: 2]
      mlflow.log_param("degree", degree)
      mlflow.log_param("test_size", test_size)
      mlflow.log_param("linspace_start", start)
      mlflow.log_param("linspace_stop", stop)
      mlflow.log_param("linspace_num", num)
      mlflow.log_param("random_state", random_state)
      mlflow.log_param("stddev", stddev)

      # Log metrics[cite: 2]
      mlflow.log_metric("train_mse", train_mse)
      mlflow.log_metric("test_mse", test_mse)
      mlflow.log_metric("mse_diff", mse_diff)
      mlflow.log_metric("mse_ratio", mse_ratio)

      print(
          f"Logged | Deg: {degree} | Test Size: {test_size} | Linspace:"
          f" ({start},{stop},{num}) | Train MSE: {train_mse:.2f} | Test MSE:"
          f" {test_mse:.2f}"
      )