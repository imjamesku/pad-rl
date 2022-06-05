from mcts import run_simulation
from ppad.pad.game import PAD
from ppad.pad.utils import cancel_until_termination

env = PAD()

combos, path = run_simulation(env.board, env.finger, prev_action=None)
print(combos, path)
for step in path:
    env.step(env.action_to_num[step])

print('Rendering gif...')
env.visualize(f"mcts/random-sim.gif")

true_combos = cancel_until_termination(env.board, skyfall_damage=False)
assert combos==len(true_combos), "combos should match"

