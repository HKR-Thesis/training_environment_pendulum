from src.deep_q_learning.deep_q_learning import DeepQLearning
from src.inverted_pendulum_simulator.src.inverted_pendulum import InvertedPendulum
import numpy as np


def simulate_episodes(num_ep: int):
    config = {
        "gamma": 1,
        "epsilon": 0.2,
        "state_dimension": 4,
        "action_dimension": 2,
        "replay_buffer_size": 300,
        "batch_replay_buffer_size": 100,
        "tn_update_period": 100,
    }

    env = InvertedPendulum()
    deep_Q_Learning = DeepQLearning(config)
    total_rewards = []

    for indexEpisode in range(num_ep):
        print(f"Simulating episode {indexEpisode}")

        rewards_ep = []
        current_state = env.reset()
        terminal = False
        while not terminal:
            action = deep_Q_Learning.select_action(current_state, indexEpisode)
            nextState, reward, terminal = env.simulate_step(action)
            rewards_ep.append(reward)
            deep_Q_Learning.replay_buffer.append(
                (current_state, action, reward, nextState, terminal)
            )
            deep_Q_Learning.train_network()
            current_state = nextState

        print(f"Sum of rewards {np.sum(rewards_ep)}")

        total_rewards.append(np.sum(rewards_ep))

    deep_Q_Learning.online_network.summary()
    deep_Q_Learning.online_network.save("trained_model-dqt.h5")
    return total_rewards
