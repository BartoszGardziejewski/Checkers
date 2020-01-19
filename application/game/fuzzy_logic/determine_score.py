from skfuzzy import control as ctrl
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting


def determine_score(white_pieces, black_pieces):
    wp = ctrl.Antecedent(np.arange(0, 12, step=1, dtype=int), 'wp')
    wp_names = ['low', 'medium_low', 'medium_high', 'high']
    wp.automf(names=wp_names)

    bp = ctrl.Antecedent(np.arange(0, 12, step=1, dtype=int), 'bp')
    bp_names = ['low', 'medium_low', 'medium_high', 'high']
    bp.automf(names=bp_names)

    score = ctrl.Consequent(np.arange(0, 50, step=1, dtype=int), 'score')
    score_names = ['losing', 'slightly_losing', 'tie', 'slightly_winning', 'winning']
    score.automf(names=score_names)

    rule_losing = ctrl.Rule(antecedent=((bp['low'] & wp['high'])
                                        | (bp['low'] & wp['medium_high'])
                                        | (bp['medium_low'] & wp['high'])),
                            consequent=score['losing'],
                            label='rule_losing')
    rule_slightly_losing = ctrl.Rule(antecedent=((bp['low'] & wp['medium_low'])
                                                 | (bp['medium_low'] & wp['medium_high'])
                                                 | (bp['medium_high'] & wp['high'])),
                                     consequent=score['slightly_losing'],
                                     label='rule_slightly_losing')
    rule_tie = ctrl.Rule(antecedent=((bp['low'] & wp['low'])
                                     | (bp['medium_low'] & wp['medium_low'])
                                     | (bp['medium_high'] & wp['medium_high'])
                                     | (bp['high'] & wp['high'])),
                         consequent=score['tie'],
                         label='rule_tie')
    rule_slightly_winning = ctrl.Rule(antecedent=((bp['medium_low'] & wp['low'])
                                                  | (bp['medium_high'] & wp['medium_low'])
                                                  | (bp['high'] & wp['medium_high'])),
                                      consequent=score['slightly_winning'],
                                      label='rule_slightly_winning')
    rule_winning = ctrl.Rule(antecedent=((bp['high'] & wp['low'])
                                         | (bp['medium_high'] & wp['low'])
                                         | (bp['high'] & wp['medium_low'])),
                             consequent=score['winning'],
                             label='rule_winning')

    system = ctrl.ControlSystem(
        rules=[rule_losing, rule_slightly_losing, rule_tie, rule_slightly_winning, rule_winning])
    simulation = ctrl.ControlSystemSimulation(system, clip_to_bounds=True)
    # view_control_space(simulation)

    simulation.input['wp'] = white_pieces
    simulation.input['bp'] = black_pieces

    simulation.compute()
    out = simulation.output['score']

    # print(out)
    # wp.view(sim=simulation)
    # bp.view(sim=simulation)
    # stage.view(sim=simulation)

    output_score = None
    max_val = 0
    for t in score.terms:
        mval = np.interp(out, score.universe, score[t].mf)
        if mval > max_val:
            max_val = mval
            output_score = t
    print(f'Score: {output_score}')

    return out


def view_control_space(sim):
    space = np.arange(0, 13)
    x, y = np.meshgrid(space, space)
    z = np.zeros_like(x)

    for wp in range(13):
        for bp in range(13):
            sim.input['wp'] = x[bp, wp]
            sim.input['bp'] = y[bp, wp]
            sim.compute()
            z[wp, bp] = sim.output['score']

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                           linewidth=0.4, antialiased=False)

    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_xlabel('white_pieces')
    ax.set_ylabel('black_pieces')
    ax.set_zlabel('score')

    ax.view_init(30, 200)
