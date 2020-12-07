from environment import Environment
from agent import DQNAgent
import pandas as pd


# possibly use denoised version of data sets
stock1 = pd.read_csv('amd')
stock2 = pd.read_csv('nvidia')

stock1.name = 'AMD'
stock2.name = 'NVDA'


def main():
    env = Environment(100000, 1, stock1, stock2)
    gamma = 0.9
    epsilon = .95
    trials = 100
    trial_len = 1460
    updateTargetNetwork = 1000
    profits = []
    dqn_agent = DQNAgent(env, stock1.name, stock2.name)
    menu_option = input("Press 0 to start fresh, Press 1 to load a model from filepath ")
    if menu_option == "1":
        dqn_agent.load_model()
    steps = []
    for trial in range(trials):
        print('Trial ', trial)
        cur_state = env.state
        step_count = 0
        start_funds = env.get_funds()
        action=''
        for step in range(trial_len):
            action_num = dqn_agent.act(cur_state)
            action, stock = None, None

            if action_num == 0:
                action, stock = 'BUY', stock1.name
            elif action_num == 1:
                action, stock = 'SELL', stock1.name
            elif action_num == 2:
                action, stock = 'BUY', stock2.name
            elif action_num == 3:
                action, stock = 'SELL', stock2.name
            elif action_num == 4:
                action, stock = 'HOLD', ''
            else:
                action, stock = None, None

            print('Step {}:'.format(step))
            print('  Action: ', action)
            print('  Stock: ', stock)
            new_state, reward, illegal_action = env.step(action, stock, 1)
            reward = reward if not illegal_action else -10000
            print('  Reward: ', reward)
            dqn_agent.remember(cur_state, action_num,
                               reward, new_state, illegal_action)

            dqn_agent.replay()
            dqn_agent.target_train()
            cur_state = new_state
            step_count += 1
            if illegal_action:
                print('Illegal action taken, starting new trial')
                break

        print('Profit: ', start_funds - env.get_funds())
        profits.append(start_funds - env.get_funds())
        env = Environment(100000, 1, stock1, stock2)
    print("Average Profit: ", sum(profits)/len(profits))
    menu_option2 = input("Press 0 to quit, press 1 to save to model to location/ ")
    if menu_option2 == "1":
        fp = input("Enter the filepath to save this model to ")
        dqn_agent.save_model(fp)

if __name__ == "__main__":
    main()
