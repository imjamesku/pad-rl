import sys,os; sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-2]))
from stable_baselines3 import PPO
from ppad.pad.combo_reward_env import ComboRewardEnv
# import sys
# print(sys.path)

model_name = "PPO_final_combo"
models_dir = f"models/{model_name}"
logdir = "logs"

env = ComboRewardEnv()
model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10000
for i in range(100000000):
    model.learn(total_timesteps=TIMESTEPS,
                reset_num_timesteps=False, tb_log_name=model_name)
    model.save(f"{models_dir}/{TIMESTEPS * i}")

episodes = 10
for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        obs, reward, done, info = env.step(env.action_space.sample())
    env.visualize(f'paths/{model_name}/{ep}.gif')
