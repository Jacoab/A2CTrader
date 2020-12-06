from collections import deque
from environment import sample_action_space
import random

from keras import Sequential, Input
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np


class DQNAgent:
    def __init__(self, env, stock1_name, stock2_name):
        self.env = env
        self.memory = deque(maxlen=2000)

        self.stock1_name = stock1_name
        self.stock2_name = stock2_name

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.01
        self.tau = 0.05
        self.model = self.create_model()
        # "hack" implemented by DeepMind to improve convergence
        self.target_model = self.create_model()

    def create_model(self):
        model = Sequential()
        state_shape = self.env.state.shape
        model.add(Dense(32, input_shape=state_shape,
                        activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(5))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            state = np.array([state])
            new_state = np.array([new_state])
            target = self.target_model.predict(state)
            if done:
                target[0, :][action] = reward
            else:
                Q_future = max(
                    self.target_model.predict(new_state)[0])
                target[0, :][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_model.set_weights(target_weights)

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        state = np.array([state])
        if np.random.random() < self.epsilon:
            return random.randint(0, 4)

        prediction = self.model.predict(state)[0]
        action = np.argmax(prediction)
        return action

    def save_model(self, fn):
        self.model.save(fn)
