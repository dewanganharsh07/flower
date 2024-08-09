"""$project_name: A Flower / FlowerTune app."""

from omegaconf import DictConfig
from flwr.common import Context, ndarrays_to_parameters
from flwr.common.config import unflatten_dict
from flwr.server import ServerAppComponents, ServerConfig
from flwr.server.strategy import FedAvg

from $import_name.client import set_parameters, get_parameters
from $import_name.models import get_model


# Get function that will be executed by the strategy's evaluate() method
# Here we use it to save global model checkpoints
def get_evaluate_fn(model_cfg, save_every_round, total_round, save_path):
    """Return an evaluation function for saving global model."""

    def evaluate(server_round: int, parameters, config):
        # Save model
        if server_round != 0 and (
            server_round == total_round or server_round % save_every_round == 0
        ):
            # Init model
            model = get_model(model_cfg)
            set_parameters(model, parameters)

            model.save_pretrained(f"{save_path}/peft_{server_round}")

        return 0.0, {}

    return evaluate


def get_on_fit_config():
    """
    Return a function that will be used to construct the config
    that the client's fit() method will receive.
    """

    def fit_config_fn(server_round: int):
        fit_config = {"current_round": server_round}
        return fit_config

    return fit_config_fn


def fit_weighted_average(metrics):
    """Aggregate (federated) evaluation metrics."""
    # Multiply accuracy of each client by number of examples used
    losses = [num_examples * m["train_loss"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"train_loss": sum(losses) / sum(examples)}


def gen_server_fn(save_path: str):  # pylint: disable=too-many-arguments
    """Generate the server function."""

    def server_fn(context: Context):
        # Read from config
        num_rounds = context.run_config["num-server-rounds"]
        cfg = DictConfig(unflatten_dict(context.run_config))

        # Get initial model weights
        init_model = get_model(cfg.model)
        init_model_parameters = get_parameters(init_model)
        init_model_parameters = ndarrays_to_parameters(init_model_parameters)

        # Define strategy
        strategy = FedAvg(
            fraction_fit=cfg.strategy.fraction_fit,
            fraction_evaluate=cfg.strategy.fraction_evaluate,
            on_fit_config_fn=get_on_fit_config(),
            fit_metrics_aggregation_fn=fit_weighted_average,
            initial_parameters=init_model_parameters,
            evaluate_fn=get_evaluate_fn(
                cfg.model, cfg.train.save_every_round, num_rounds, save_path
            ),
        )

        config = ServerConfig(num_rounds=num_rounds)

        return ServerAppComponents(strategy=strategy, config=config)

    return server_fn
