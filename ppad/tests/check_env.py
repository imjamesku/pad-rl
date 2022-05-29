import sys,os; sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-3]))
from stable_baselines3.common.env_checker import check_env
from ppad.pad.game import PAD

env = PAD()
# It will check your custom environment and output additional warnings if needed
# print(env.observation_space)
# print("state")
obs = env.reset()
# print(obs)
# print(obs.shape)
# print(obs.dtype)
# check_env(env)
