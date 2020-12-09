# Deep Q Network Trader
Final project of Jake Jongewaard and Raymond Wu for CSCI 4800.  Here we use a deep q network with expierence replay to learn profitable stock trading strategies.

* Data can be found in the /data directory
* complex_model_0 - The model trained on Adobe and Apple stock data
* complex_model_1 - The model trained on AMD and Nvidia stock data
* old_models - Previous trial models using the sparse reward function in the Environment class
* environment.py - Environment class that allows buying, selling and holding of stocks
* agent.py - Deep Q Network implementation
* datacollect.py - Script for collection data (requires Quandl key)
* trader.py - Training script for the environment and DQAgent
