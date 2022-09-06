import random

from deap import base, creator, tools
from copy import deepcopy

import warnings
warnings.simplefilter("ignore")


# define the payoff matrix
tc1_payoffs = {"00":[5,5],"01":[8,4],"11":[0,0],"10":[4,8]}
# your code goes here	
tc2_payoffs = {"00":[12,12],"01":[13,11],"11":[12,12],"10":[11,13]}
# your code goes here	


# exercise 2(a)
def payoff_to_player1(player1, player2, game):
    # your code goes here
    tc_matrix_val = str(player1[len(player1)-1]) + str(player2[len(player2)-1])
    print(game)
    payoff = game.get(tc_matrix_val)
    return payoff


# exercise 2(b)
def next_move(player1, player2, round):    
    #your code goes here
    tmp = 0
    decimal_val = 0
    player1_move = []
    pl1_pos = 0
    pl2_pos = 0
    if round == 0 or (len(player1) == 18 and len(player2) == 18): #checks if round is 0 meaning the game has just started or if either of players lengths are 18 meaning they have no memory bits
        for idx in range(len(player1)):
            if (len(player1) == 18 and len(player2) == 18) and (idx == 16 or idx == 17): #if the length of both players is 18 then the default bits will be appended to the end of each player and used as a move
                player1.append(player1[idx])
                player2.append(player2[idx])
            if idx == 17:
                player1_move.append(player1[idx])
                player1_move.append(player2[idx])
        return player1_move
    elif round >= 1:
        tmp = str(player1[len(player1)-1]) + str(player1[len(player1)-2]) + str(player2[len(player2)-1]) + str(player2[len(player2)-2])
        decimal_val = int(tmp, 2)
        pl1_pos = player1[decimal_val]
        pl2_pos = player2[decimal_val]
        player1_move.append(pl1_pos)
        player1_move.append(pl2_pos)
    return player1_move #returns list with moves for player1 and player2 found in their respective strategy bits

# exercise 2(c)
def process_move(player, move, memory_depth):
    # your code goes here
    del player[len(player)-memory_depth]#deletes old memory bits and adds on new bits retrieved from the strategy bits
    player.append(move)
    if len(player) == 20 and player[len(player)-1] == move: #ensures if the process was done correctly by checking the size of the player and new memory bits values are the same as the move 
        return True
    else:
        return False


# exercise 2(d)
def score(player1, player2, m_depth, n_rounds, game):
    # your code goes here
    score_to_player1 = 0
    score_to_player2 = 0
    move_list = []
    move_pl1 = 0
    move_pl2 = 0
    payoff_pl = 0
    #print("pl1" , player1)
    #print("pl2" , player2)
    for i in range(n_rounds):
        move_list = []
        move_list = next_move(player1, player2, i)
        move_pl1 = move_list[0]
        move_pl2 = move_list[1]
        process_move(player1, move_pl1, m_depth) #process both player1 and player2 to ensure they are both up to date with current data and reflects the correct functionality of the spec
        process_move(player2, move_pl2, m_depth)
        payoff_pl = payoff_to_player1(player1, player2, game)
        score_to_player1 += payoff_pl[0]
        score_to_player2 += payoff_pl[1]
    return score_to_player1

def eval_func(individual, individual2):
    game = tc
    return score(individual,individual2,mem_depth,n_rounds,game),

# Create the toolbox with the right parameters
def create_toolbox(num_bits):
    # your code goes here
    
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("individual", list, fitness=creator.FitnessMax)
    

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.individual,
                 toolbox.attr_bool, num_bits)
    toolbox.register("population1", tools.initRepeat, list, toolbox.individual)
    toolbox.register("population2", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", eval_func)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    return toolbox


# This function implements the evolutionary algorithm for the game
def play_game(mem_depth, population1_size, generation_size, n_rounds, game):   
    mem_depth = 2
    num_bits = pow(2,(2*mem_depth))+(2*mem_depth)	# your code goes here: calculate the bits using the mem_depth value
    
    # Create a toolbox using the above parameter
    toolbox = create_toolbox(num_bits)
    
    # Seed the random number generator
    random.seed(3)

    # Create an initial population1 of n individuals
    population1 = toolbox.population1(n = population1_size)
    population2 = toolbox.population2(n = population1_size)

    # Define probabilities of crossing and mutating
    probab_crossing, probab_mutating  = 0.5, 0.2    
    
    print('\nStarting the evolution process')
    
    # Evaluate the entire population1
    # your code goes here:
 
    #Using DEAP documentation and week 8 tutorial the onemax GA was applied
    fitnesses = list(map(toolbox.evaluate, population1, population2))
    
	# Calculate the fitness value for each player.
	# Each player will play against every other player in the population1.
	# The fitness values of a player is the total score of all games played against every other players.    
    
    print('\nEvaluated', len(population1), 'individuals')

    for ind, fit in zip(population1, fitnesses):
        ind.fitness.values = fit
 
    # Iterate through generations
    for g in range(generation_size):
        print("\n===== Generation", g)
        # your code goes here
		# apply the steps of the evolutionary algorithm

          # Extracting all the fitnesses of 
        fits = [ind.fitness.values[0] for ind in population1]
        offspring = toolbox.select(population1, len(population1))
        offspring = list(map(toolbox.clone, offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < probab_crossing:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < probab_mutating:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print("  Evaluated %i individuals" % len(invalid_ind))
        population1[:] = offspring
        fits = [ind.fitness.values[0] for ind in population1]
        length = len(population1)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
    
    print("-- End of (successful) evolution --")


if __name__ == "__main__":
    mem_depth = 2
    population1_size = 10
    generation_size = 5
    n_rounds = 4
    tc = 0

    print('===================')
    print('Play the game ITC1')
    print('===================')
    tc = tc1_payoffs
    play_game(mem_depth, population1_size, generation_size, n_rounds, tc)

    print('\n\n===================')
    print('Play the game ITC2')
    print('===================')
    tc = tc2_payoffs
    play_game(mem_depth, population1_size, generation_size, n_rounds, tc)
