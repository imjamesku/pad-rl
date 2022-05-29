import sys,os; sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-2]))
from stable_baselines3 import PPO
from ppad.pad.combo_reward_env import ComboRewardEnv
# import sys
# print(sys.path)

model_name = "PPO_final_combo"
model_path = "models/PPO_final_combo/29000.zip"
models_dir = f"models/{model_name}"
logdir = "logs"

env = ComboRewardEnv()
model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

model.load(model_path, env=env)

episodes = 10
for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        obs, reward, done, info = env.step(env.action_space.sample())
    env.visualize(f'{ep}.gif')
