import tensorflow as tf
import pandas as pd
import numpy as np
from environment import Environment

model = tf.keras.models.load_model('complex_model_0')
stock1 = pd.read_csv('data/adobe-test.csv')
stock2 = pd.read_csv('data/apple-test.csv')

stock1.name = 'ADBE'
stock2.name = 'AAPL'

trial_len = 1030
env = Environment(100000, 1, trial_len, stock1, stock2)

stock1_buys = 0
stock1_sells = 0
stock2_buys = 0
stock2_sells = 0
holds = 0
start_funds = env.get_funds()
cur_state = env.state
for step in range(trial_len):
    print('State: ', env.get_past_5_days_open_avg())
    prediction = model.predict(np.array([cur_state]))[0]
    print(prediction)
    action_num = np.argmax(prediction)
    action, stock = None, None

    #print('Action Number: ', action_num)
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

    print('Step {}:'.format(step))
    print('  Action: ', action)
    print('  Stock:  ', stock)
    cur_state, reward, illegal_action = env.step(action, stock, 1)
    #print('After state: ', cur_state)
    if illegal_action:
        print('Illegal action taken')
        break

end_funds = env.get_funds()
print('Profit: ', end_funds - start_funds)