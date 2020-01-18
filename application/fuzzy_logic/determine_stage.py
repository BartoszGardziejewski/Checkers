from skfuzzy import control as ctrl
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting


def determine_stage(completed_turns_number, total_pieces_number):
    turns = ctrl.Antecedent(np.arange(0, 200, step=1, dtype=int), 'turns')
    turns_names = ['low', 'medium', 'high']
    turns.automf(names=turns_names)

    pieces = ctrl.Antecedent(np.arange(0, 24, step=1, dtype=int), 'pieces')
    pieces_names = ['low', 'medium', 'high']
    pieces.automf(names=pieces_names)

    stage = ctrl.Consequent(np.arange(0, 4, step=1, dtype=int), 'stage')
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

    view_control_space(simulation)

    simulation.input['turns'] = completed_turns_number
    simulation.input['pieces'] = total_pieces_number

    simulation.compute()

    print(simulation.output['stage'])

    # stage.view(sim=simulation)
    plt.show()

    return simulation.output['stage']


def view_control_space(sim):
    x_space = np.arange(0, 201)
    y_space = np.arange(0, 25)
    x, y = np.meshgrid(x_space, y_space)
    z = np.zeros_like(x)

    for turns in range(201):
        for pieces in range(25):
            sim.input['turns'] = x[pieces, turns]
            sim.input['pieces'] = y[pieces, turns]
            sim.compute()
            z[pieces, turns] = sim.output['stage']

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                           linewidth=0.4, antialiased=False)

    ax.set_xlabel('turns')
    ax.set_ylabel('pieces')
    ax.set_zlabel('stage')

    ax.view_init(30, 200)
