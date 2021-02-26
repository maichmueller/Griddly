import os
import sys

import ray
from ray import tune
from ray.rllib.models import ModelCatalog
from ray.tune.registry import register_env

from griddly import gd
from griddly.util.rllib import RLlibMultiAgentWrapper
from griddly.util.rllib.torch import GAPAgent
from griddly.util.rllib.torch.impala.impala import InvalidActionMaskingImpalaTrainer


class GridnetAgent(object):
    pass


if __name__ == '__main__':
    sep = os.pathsep
    os.environ['PYTHONPATH'] = sep.join(sys.path)

    ray.init(num_gpus=1)

    env_name = 'ray-griddly-rts-env'

    test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'GriddlyRTS_test.yaml')

    register_env(env_name, RLlibMultiAgentWrapper)
    ModelCatalog.register_custom_model('GridnetAgent', GridnetAgent)

    config = {
        'framework': 'torch',
        'num_workers': 8,
        'num_envs_per_worker': 1,

        'model': {
            'custom_model': 'GridnetAgent',
            'custom_model_config': {}
        },
        'env': env_name,
        'env_config': {
            'record_video_config': {
                'frequency': 100000  # number of rollouts
            },

            'yaml_file': test_path,
            'global_observer_type': gd.ObserverType.ISOMETRIC,
            'level': 1,
            'max_steps': 1000,
        },
        'lr': tune.grid_search([0.0001, 0.0005, 0.001, 0.005])
    }

    stop = {
        'timesteps_total': 200000000,
    }

    result = tune.run(InvalidActionMaskingImpalaTrainer, config=config, stop=stop)
