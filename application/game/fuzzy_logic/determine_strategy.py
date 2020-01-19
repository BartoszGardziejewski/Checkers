from enum import Enum

from skfuzzy import control as ctrl
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting


class Strategy(Enum):
    defensive = 1,
    slightly_defensive = 2,
    slightly_aggressive = 3,
    aggressive = 4


def determine_strategy(stage_input, score_input):
    stage = ctrl.Antecedent(np.arange(0, 40, step=1, dtype=int), 'stage')
    stage_names = ['beginning', 'early_middle', 'late_middle', 'endgame']
    stage.automf(names=stage_names)

    score = ctrl.Antecedent(np.arange(0, 50, step=1, dtype=int), 'score')
    score_names = ['losing', 'slightly_losing', 'tie', 'slightly_winning', 'winning']
    score.automf(names=score_names)

    strategy = ctrl.Consequent(np.arange(0, 40, step=1, dtype=int), 'strategy')
    strategy_names = ['defensive', 'slightly_defensive', 'slightly_aggressive', 'aggressive']
    strategy.automf(names=strategy_names)

    rule_defensive = ctrl.Rule(antecedent=(score['losing'] | (stage['beginning'] & score['slightly_losing'])),
                               consequent=strategy['defensive'],
                               label='rule_defensive')
    rule_slightly_defensive = ctrl.Rule(antecedent=((stage['early_middle'] & score['slightly_losing'])
                                                    | (stage['late_middle'] & score['slightly_losing'])
                                                    | (stage['endgame'] & score['slightly_losing'])
                                                    | (stage['early_middle'] & score['tie'])
                                                    | (stage['late_middle'] & score['tie'])
                                                    | (stage['early_middle'] & score['slightly_winning'])),
                                        consequent=strategy['slightly_defensive'],
                                        label='rule_slightly_defensive')
    rule_slightly_aggressive = ctrl.Rule(antecedent=((stage['beginning'] & score['tie'])
                                                     | (stage['endgame'] & score['tie'])
                                                     | (stage['beginning'] & score['slightly_winning'])
                                                     | (stage['late_middle'] & score['slightly_winning'])
                                                     | (stage['beginning'] & score['winning'])
                                                     | (stage['early_middle'] & score['winning'])),
                                         consequent=strategy['slightly_aggressive'],
                                         label='rule_slightly_aggressive')
    rule_aggressive = ctrl.Rule(antecedent=((stage['endgame'] & score['slightly_winning'])
                                            | (stage['endgame'] & score['winning'])
                                            | (stage['late_middle'] & score['winning'])),
                                consequent=strategy['aggressive'],
                                label='rule_aggressive')

    system = ctrl.ControlSystem(
        rules=[rule_defensive, rule_slightly_defensive, rule_slightly_aggressive, rule_aggressive])
    simulation = ctrl.ControlSystemSimulation(system, clip_to_bounds=True)

    simulation.input['stage'] = stage_input
    simulation.input['score'] = score_input

    simulation.compute()
    out = simulation.output['strategy']

    # view_control_space(simulation)
    # print(simulation.output['strategy'])
    # strategy.view(sim=simulation)

    output_strategy = None
    max_val = 0
    for t in strategy.terms:
        mval = np.interp(out, strategy.universe, strategy[t].mf)
        if mval > max_val:
            max_val = mval
            output_strategy = Strategy[t]

    return output_strategy


def view_control_space(sim):
    x_space = np.arange(0, 41)
    y_space = np.arange(0, 51)
    x, y = np.meshgrid(x_space, y_space)
    z = np.zeros_like(x)

    for stage in range(40):
        for score in range(50):
            sim.input['stage'] = x[score, stage]
            sim.input['score'] = y[score, stage]
            sim.compute()
            z[score, stage] = sim.output['strategy']

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                           linewidth=0.4, antialiased=False)

    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_xlabel('stage')
    ax.set_ylabel('score')
    ax.set_zlabel('strategy')

    ax.view_init(30, 200)
