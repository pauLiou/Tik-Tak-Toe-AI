import gym
import numpy as np
import random
import environment
from keras.models import Sequential
from keras.layers import Dense

# Create the Tic-Tac-Toe environment
env = environment.TikTacToeEnv()

# Set the learning rate (alpha) and discount factor (gamma)
alpha = 0.1
gamma = 0.6
epsilon = 1.0

# Set the number of episodes to train for
num_episodes = 10000

# Create the model
model = Sequential()
model.add(Dense(24, input_dim=3, activation='relu'))
model.add(Dense(48, activation='relu'))
model.add(Dense(3, activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

# Train the model
for i in range(num_episodes):
    # Reset the environment
    state = env.reset()
    
    # Set the initial reward
    reward = 0
    
    # Set the initial done flag
    done = False
    
    # Loop until the episode is done
    while not done:
        # Choose an action according to the epsilon-greedy policy
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, 2)
        else:
            action = np.argmax(model.predict(np.array([state]))[0])

        
        
        # Take the action and observe the next state, reward, and done flag
        next_state, reward, done, _ = env.step(action)
        
        # Calculate the target Q-value
        target = reward + gamma * np.amax(model.predict(np.array([next_state]))[0])
        
        # Calculate the Q-value of the current state-action pair
        q_value = model.predict(np.array([state]))
        q_value[0][action] = target
        
        # Train the model on the current state-action pair
        model.fit(np.array([state]), q_value, epochs=1, verbose=0)
        
        # Set the current state to the next state
        state = next_state


# Test the model
state = env.reset()
done = False
while not done:
    action = np.argmax(model.predict(np.array([state]))[0])
    state, reward, done, _ = env.step(action)
    env.render()