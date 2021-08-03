import itertools
from dice_game import DiceGame
game = DiceGame()
import numpy as np
from abc import ABC, abstractmethod


class DiceGameAgent(ABC):
    def __init__(self, game):
        self.game = game
    
    @abstractmethod
    def play(self, state):
        pass


class AlwaysHoldAgent(DiceGameAgent):
    def play(self, state):
        return (0, 1, 2)


class PerfectionistAgent(DiceGameAgent):
    def play(self, state):
        if state == (1, 1, 1) or state == (1, 1, 6):
            return (0, 1, 2)
        else:
            return ()
        
        
def play_game_with_agent(agent, game, verbose=True):
    state = game.reset()
    
    if(verbose): print(f"Testing agent: \n\t{type(agent).__name__}")
    if(verbose): print(f"Starting dice: \n\t{state}\n")
    
    game_over = False
    actions = 0
    while not game_over:
        action = agent.play(state)
        actions += 1
        
        if(verbose): print(f"Action {actions}: \t{action}")
        _, state, game_over = game.roll(action)
        if(verbose and not game_over): print(f"Dice: \t\t{state}")

    if(verbose): print(f"\nFinal dice: {state}, score: {game.score}")
        
    return game.score


if __name__ == "__main__":
    # random seed makes the results deterministic
    # change the number to see different results
    # or delete the line to make it change each time it is run
    np.random.seed(1)
    
    game = DiceGame()
    
   # agent1 = AlwaysHoldAgent(game)
    #play_game_with_agent(agent1, game, verbose=True)
    
    print("\n")
    
    #agent2 = PerfectionistAgent(game)
    #play_game_with_agent(agent2, game, verbose=True)

    class MyAgent(DiceGameAgent):
        def __init__(self, game):
            
            """
            if your code does any pre-processing on the game, you can do it here
            
            e.g. you could do the value iteration algorithm here once, store the policy, 
            and then use it in the play method
            
            you can always access the game with self.game
            """
            # this calls the superclass constructor (does self.game = game)
            super().__init__(game) 
            
            # YOUR CODE HERE
            self.gamma = 0.9
            self.theta = 0.1

            
        def play(self, state):
            """
            given a state, return the chosen action for this state
            at minimum you must support the basic rules: three six-sided fair dice
            
            if you want to support more rules, use the values inside self.game, e.g.
                the input state will be one of self.game.states
                you must return one of self.game.actions
            
            read the code in dicegame.py to learn more
            """
            # YOUR CODE HERE          
            v = self.val_iteration()
            policy = self.find_best_actions(v)
            return policy


        def utility_dictionary(self):
            util = {}
            for s in game.states:
                util[s] = 0
            return util
 
        
        def max_action(self, state, util):
            maximum = 0
            for a in game.actions:
                next_states, _, reward, probabilities = game.get_next_states(a, state)
                temp = 0
                for next_state, prob in zip(next_states, probabilities):
                    if next_state is None:
                        u = 0
                    else: 
                        u = util[next_state]
                    temp = temp + prob * (reward + self.gamma * u)
            if temp > maximum:
                maximum = temp 
            return maximum, a


        def val_iteration(self):   
            v = self.utility_dictionary()
            while True:            
                delta = 0
                for s in game.states:  
                    temp = v[s] 
                    v[s], _ = self.max_action(s, v)
                    delta = max(delta, np.abs(temp - v[s]))
                if delta < self.theta:
                    break
            return v
            

        def find_best_actions(self, v):
            policy = {}
            # for each state in the dictionary, find the best action 
            for s in v:
                _, policy[s] = self.max_action(s, v)
                best_action = max(policy.values())
            return best_action


      #TESTING
import time

total_score = 0
total_time = 0
n = 10

np.random.seed()

print("Testing basic rules.")
print()

game = DiceGame()

start_time = time.process_time()
test_agent = MyAgent(game)
total_time += time.process_time() - start_time

for i in range(n):
    start_time = time.process_time()
    score = play_game_with_agent(test_agent, game)
    total_time += time.process_time() - start_time

    print(f"Game {i} score: {score}")
    total_score += score

print()
print(f"Average score: {total_score/n}")
print(f"Total time: {total_time:.4f} seconds")