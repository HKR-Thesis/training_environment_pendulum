# you will also need to install MoviePy, and you do not need to import it explicitly
# pip install moviepy

# import Keras
import keras

# import the class
from src.deep_q_learning.deep_q_learning import DeepQLearning
from ..inverted_pendulum_simulator.src.inverted_pendulum import InvertedPendulum
from ..inverted_pendulum_simulator.src.inverted_pendulum_visualizer import (
    InvertedPendulumVisualizer,
)


# numpy
import numpy as np


def simulate_model(loaded_model, episodes: int) -> None:
    env = InvertedPendulum()
    env.reset()
    visualizer = InvertedPendulumVisualizer(env)
    states = []

    for _ in range(episodes):
        states.append(env.state)
        Qvalues = loaded_model.predict([env.state])
        action = np.random.choice(np.where(Qvalues[0, :] == np.max(Qvalues[0, :]))[0])
        env.simulate_step(action)

    visualizer.animate_states(states)


if __name__ == "__main__":
    loaded_model = keras.models.load_model(
        "trained_model-dqt.h5", custom_objects={"loss_fn": DeepQLearning.loss_fn}
    )
    simulate_model(loaded_model, 500)
