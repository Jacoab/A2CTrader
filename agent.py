from collections import deque
from environment import sample_action_space
import random

from keras import Sequential
import keras
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import *
import numpy as np


class DQNAgent:
    def __init__(self, env, stock1_name, stock2_name):
        # Deep Q network agent with expierence replay
        self.env = env
        self.memory = deque(maxlen=2000)

        self.stock1_name = stock1_name
        self.stock2_name = stock2_name

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.0001
        self.tau = 0.05
        self.model = self.create_model()
        # "hack" implemented by DeepMind to improve convergence
        self.target_model = self.create_model()

    # Loads a model using self.filepath
    def load_model(self):
        fp = input("Enter the name of your model folder ")
        # change below
        self.model = load_model(fp)

    # Creates the model using keras
    def create_model(self):
        model = Sequential()
        state_shape = self.env.state.shape
        model.add(Dense(32, input_shape=state_shape,
                        activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(5))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        return model

    # saves state, action, reward, newstate, done pairs
    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    # Expierence replay with vectorized operations
    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)

        states = np.array([np.array(sample[0]) for sample in samples])
        actions = np.array([sample[1] for sample in samples])
        rewards = np.array([sample[2] for sample in samples])
        next_states = np.array([np.array(sample[3]) for sample in samples])
        done = np.array([sample[4] for sample in samples])

        target = rewards + self.gamma * np.amax(self.model.predict(next_states), axis=1)
        target[done] = rewards[done]

        target_f = self.model.predict(states)
        target_f[range(batch_size), actions] = target

        self.model.fit(states, target_f, epochs=1, verbose=0)

    # Transfers weights to target network
    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_model.set_weights(target_weights)

    # generates an action, generates a random action if epsilon is less than a random number
    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        state = np.array([state])
        if np.random.random() < self.epsilon:
            print('  random act')
            return random.randint(0, 4)

        print('  nn act')
        prediction = self.model.predict(state)[0]
        action = np.argmax(prediction)
        return action

    # Saves model to specified path
    def custom_save_model(self, fullpath):
        self.model.save(fullpath)
