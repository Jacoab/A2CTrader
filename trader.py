from environment import Environment
from agent import DQNAgent
import pandas as pd
import random


stock1 = pd.read_csv('data/amd-train.csv')
stock2 = pd.read_csv('data/nvidia-train.csv')

stock1.name = 'AMD'
stock2.name = 'NVDA'


def main():
    trial_len = 1030

    env = Environment(100000, 1, trial_len, stock1, stock2)
    trials = 100

    action_info = {
        's1_buys_per_trial': [],
        's1_sells_per_trial': [],
        's2_buys_per_trial': [],
        's2_sells_per_trial': [],
        'holds_per_trial': [],
        'illegal_action_trial': [],
        'profits_per_trial': [],
        'ranges_per_trial': [],
        'good_profits_and_range': []
    }

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

        stock1_buys = 0
        stock1_sells = 0
        stock2_buys = 0
        stock2_sells = 0
        holds = 0
        illegal_action = False
        returns = []

        for step in range(trial_len):
            action_num = dqn_agent.act(cur_state)
            action, stock = None, None

            # Get action from Deep Q Net output
            if action_num == 0:
                action, stock = 'BUY', stock1.name
                stock1_buys += 1
            elif action_num == 1:
                action, stock = 'SELL', stock1.name
                stock1_sells += 1
            elif action_num == 2:
                action, stock = 'BUY', stock2.name
                stock2_buys += 1
            elif action_num == 3:
                action, stock = 'SELL', stock2.name
                stock2_sells += 1
            elif action_num == 4:
                action, stock = 'HOLD', ''
                holds += 1
            else:
                action, stock = None, None

            prev_funds = env.get_funds()
            print('Step {}:'.format(step))
            print('  Action: ', action)
            print('  Stock:  ', stock)
            new_state, reward, illegal_action = env.step(action, stock, 1)
            reward = reward if not illegal_action else -10000
            new_funds = env.get_funds()
            returns.append(new_funds-prev_funds)
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

        profit = start_funds - env.get_funds()
        df_range = (env.init_day_index, env.init_day_index + trial_len)
        print('Profit: ', start_funds - env.get_funds())

        if profit >= 5000.00:
            action_info['good_profits_and_range'].append((df_range, returns))
            print(action_info['good_profits_and_range'])

        action_info['profits_per_trial'].append(profit)

        action_info['s1_buys_per_trial'].append(stock1_buys)
        action_info['s1_sells_per_trial'].append(stock1_sells)
        action_info['s2_buys_per_trial'].append(stock2_buys)
        action_info['s2_sells_per_trial'].append(stock2_sells)
        action_info['holds_per_trial'].append(holds)
        action_info['illegal_action_trial'].append(illegal_action)
        action_info['ranges_per_trial'].append((env.init_day_index, env.init_day_index + trial_len))

        n = random.randint(0, len(stock1) - trial_len)
        env = Environment(100000, 1, trial_len, stock1, stock2)

    print("Average Profit: ", sum(action_info['profits_per_trial'])/len(action_info['profits_per_trial']))
    data_file_name = input('Please type the name of the file you would like to save the action info to: ')
    menu_option2 = input("Press 0 to quit, press 1 to save to model to location/ ")
    if menu_option2 == "1":
        fp = input("Enter the filepath to save this model to ")
        dqn_agent.custom_save_model(fp)

    action_info_df = pd.DataFrame(action_info)
    action_info_df.to_csv(data_file_name)


if __name__ == "__main__":
    main()
