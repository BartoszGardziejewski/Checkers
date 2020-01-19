from skfuzzy import control as ctrl
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting


def determine_stage(completed_turns_number, losing_player_pieces):
    turns = ctrl.Antecedent(np.arange(0, 50, step=1, dtype=int), 'turns')
    turns_names = ['low', 'medium', 'high']
    turns.automf(names=turns_names)

    pieces = ctrl.Antecedent(np.arange(0, 12, step=1, dtype=int), 'pieces')
    pieces_names = ['low', 'medium', 'high']
    pieces.automf(names=pieces_names)

    stage = ctrl.Consequent(np.arange(0, 40, step=1, dtype=int), 'stage')
    stage_names = ['beginning', 'early_middle', 'late_middle', 'endgame']
    stage.automf(names=stage_names)

    rule_beginning = ctrl.Rule(antecedent=(turns['low'] & pieces['high']),
                               consequent=stage['beginning'],
                               label='rule_beginning')
    rule_early_middle = ctrl.Rule(antecedent=((turns['low'] & pieces['medium'])
                                              | (turns['medium'] & pieces['high'])
                                              | (turns['high'] & pieces['high'])),
                                  consequent=stage['early_middle'],
                                  label='rule_early_middle')
    rule_late_middle = ctrl.Rule(antecedent=((turns['low'] & pieces['low'])
                                             | (turns['medium'] & pieces['medium'])
                                             | (turns['high'] & pieces['medium'])),
                                 consequent=stage['late_middle'],
                                 label='rule_late_middle')
    rule_endgame = ctrl.Rule(antecedent=((turns['medium'] & pieces['low'])
                                         | (turns['high'] & pieces['low'])),
                             consequent=stage['endgame'],
                             label='rule_endgame')

    system = ctrl.ControlSystem(rules=[rule_beginning, rule_early_middle, rule_late_middle, rule_endgame])
    simulation = ctrl.ControlSystemSimulation(system, clip_to_bounds=True)

    simulation.input['turns'] = completed_turns_number
    simulation.input['pieces'] = losing_player_pieces

    simulation.compute()
    out = simulation.output['stage']

    # view_control_space(simulation)
    # print(simulation.output['stage'])
    # stage.view(sim=simulation)

    output_stage = None
    max_val = 0
    for t in stage.terms:
        mval = np.interp(out, stage.universe, stage[t].mf)
        if mval > max_val:
            max_val = mval
            output_stage = t
    print(f'Stage of the game: {output_stage}')

    return out


def view_control_space(sim):
    x_space = np.arange(0, 101)
    y_space = np.arange(0, 13)
    x, y = np.meshgrid(x_space, y_space)
    z = np.zeros_like(x)

    for turns in range(101):
        for pieces in range(13):
            sim.input['turns'] = x[pieces, turns]
            sim.input['pieces'] = y[pieces, turns]
            sim.compute()
            z[pieces, turns] = sim.output['stage']

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                           linewidth=0.4, antialiased=False)

    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_xlabel('turns')
    ax.set_ylabel('pieces')
    ax.set_zlabel('stage')

    ax.view_init(30, 200)
