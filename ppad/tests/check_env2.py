import sys,os; sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-3]))
from stable_baselines3.common.env_checker import check_env
from ppad.pad.game import PAD
from ppad.pad.combo_reward_env import ComboRewardEnv

# env = PAD()
env = ComboRewardEnv()
# It will check your custom environment and output additional warnings if needed
# print(env.observation_space)
# print("state")
obs = env.reset()
# print(obs)
# print(obs.shape)
# print(obs.dtype)
check_env(env)

episodes = 10
for ep in range(episodes):
    print('ep: ', ep)
    done = False
    while not done:
        obs, reward, done, info = env.step(env.action_space.sample())
    # print('obs len', len(env.game.observations))
    # print('actions len', len(env.game.actions))
    env.visualize(f'output/{ep}.gif')
    env.reset()
