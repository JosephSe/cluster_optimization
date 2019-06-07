from common import args
from common.util import timed

from env import Env

import os
import numpy as np

from models import Stochastic
from models import RoundRobin
from models import Greedy
from models import learn_local
from models import learn_hierarchical


if __name__ == '__main__':
    env = Env()

    models = [
        RoundRobin(act_size=args.n_servers),

        Stochastic(act_size=args.n_servers),

        Greedy(act_size=args.n_servers, n_servers=args.n_servers),

        learn_local(
            env=env,
            total_epoches=args.total_epoches,
            n_servers=args.n_servers,
            l_ob_size=args.l_obsize + 1,
            l_act_size=args.l_actsize,
            l_latents=args.l_latents,
            l_lr=args.l_lr,
            l_ac=args.l_ac,
        ),

        learn_hierarchical(
            env=env,
            batch_size=args.batch_size,
            total_epoches=args.total_epoches,
            gamma=0.8,
            g_ob_size=args.n_servers * args.n_resources + args.n_resources + 1,
            g_act_size=args.n_servers,
            g_latents=args.g_latents,
            g_lr=args.g_lr,
            g_ac=args.g_ac,
            l_ob_size=args.l_obsize + 1,
            l_act_size=args.l_actsize,
            l_latents=args.l_latents,
            l_lr=args.l_lr,
            l_ac=args.l_ac,
        )
    ]

    for model in models:
        done = False
        obs = env.reset(model.local_model, model.predictor)
        while not done:
            action = int(model.step(obs))
            _, _, done, info = env.step(action)

        power_usage, latency = info

        np.savetxt(os.path.join('logs', f'{model.name}_power.txt'), power_usage)
        np.savetxt(os.path.join('logs', f'{model.name}_latency.txt'), latency)
