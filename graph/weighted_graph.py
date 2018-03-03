import math
from graph.get_curr import *

def create_distance_table(curr):

    distances = {}
    for currency in curr:
        distances[currency] = float('inf')                  # set all starting vertices to be infinite distance away
    return distances

def create_predecessor_table(curr):

    predecessor = {}
    for currency in curr:
        predecessor[currency] = None                        # set all starting vertices to have no predecessor
    return predecessor

def show_negative_weight_cycle(predecessors, node):

    print ('NEGATIVE CYCLE')
    print ('PRED: ' + str(predecessors))
    print ('NODE: ' + node)

    arbitrage = [node]                                      # temp list used to display currencies with arbitrage opportunities
    next_node = predecessors[node]

    while next_node not in arbitrage:
        arbitrage.append(next_node)
        next_node = predecessors[next_node]

    arbitrage.append(next_node)
    arbitrage = arbitrage[arbitrage.index(next_node):]      # nodes appended in backwards order of arbitrage
    arbitrage = arbitrage[::-1]                             # reverse order of list to get arbitrage opportunites in forward order
    return arbitrage


#####################################################        WEIGHTED GRAPH      #####################################################

class weighted_graph:

    def __init__(self, currs):

        self.currencies = currs                                             # list of currencies
        self.curr_df, self.curr_matrix, self.table_dict = get_data(currs)   # currency data frame (with listings of all edges)
        #print('TESTING WEIGHTED GRAPH')
        #print (self.curr_df)
        #print ('\n')

    def get_weight(self, edge):

        edge_rate = self.curr_df.get_value(edge, 'edge_weight')             # edge weights based on NEGATIVE LOG-EXCHANGE RATE
        return edge_rate

    def get_time(self):

        return self.curr_df['timestamp'].iloc[0]                            # return timestamp at first row

    def get_default_weight(self, edge):

        edge_rate = self.curr_df.get_value(edge, 'ask')                     # edge weights based on ASK RATE
        return edge_rate

    def bellmanford(self, start):

        updated = True                                                      # keeps track of whether an update was made or not
        iteration = 1                                                       # keeps track of the iteration number
        num_currencies = len(self.currencies)                               # number of currencies
        currency_list = self.currencies                                     # temp list to store currencies

        dist_table = create_distance_table(currency_list)
        dist_table[start] = 0                                               # set up start node
        pre_table = create_predecessor_table(currency_list)                 # predecessor table

        # FIRST |V-1| ITERATIONS
        while iteration < num_currencies and updated == True:
            #print (dist_table)             # shortest path table
            #print (pre_table)              # predecessor table
            updated = False                                                 # reset updated for checking if an update occurs later
            for from_curr in currency_list:                                 # First Loop for each currency
                for to_curr in currency_list:                               # Second Loop for each currency that
                    if dist_table[from_curr] + self.get_weight(from_curr + to_curr) < dist_table[to_curr]:              # if a shorter path is found to THIS node
                        dist_table[to_curr] = dist_table[from_curr] + self.get_weight(from_curr + to_curr)              # update distance table with shorter path distance
                        pre_table[to_curr] = from_curr                                                                  # update predecessor table with shorter path node
                        updated = True                                                                                  # an update occurred so updated = True
                        print ('(1): ' + from_curr + ' TO ' + to_curr)
                        print (str(dist_table))
                        print (str(pre_table) + '\n')

            iteration = iteration + 1

        #print (dist_table)             # shortest path table
        #print (pre_table)              # predecessor table
        #print ('\n')

        print ('NEGATIVE DETECTION ALGO')

        # FINAL ITERATION to detect NEGATIVE WEIGHT CYCLES
        if updated == True:
            for from_curr in currency_list:                             # First Loop for each currency
                for to_curr in currency_list:                           # Second Loop for each currency that

                    if dist_table[from_curr] + self.get_weight(from_curr + to_curr) < dist_table[to_curr]:    # negative cycle detected
                        # Display the arbitrage opportunity using the predecessors table
                        return show_negative_weight_cycle(pre_table, start)

        # No negative cycles detected
        return None

    def show_arbitrage_opportunities(self):

        arbitrage_opportunities = []
        print ('START' + str(self.currencies))
        for curr in self.currencies:
            print ('-----------------------' + curr)
            arbitrage = self.bellmanford(curr)
            print (arbitrage)
            if arbitrage is not None and arbitrage not in arbitrage_opportunities:      # if a new potential arbitrage opportunity exists

                # Test the arbitrage opportunity for more than 2% yield per cycle
                arb_yield = 1
                for i in range (1, len(arbitrage)):
                    edge = arbitrage[i-1] + arbitrage[i]                                # string value representing the edge
                    print (edge)
                    arb_yield = arb_yield * self.get_default_weight(edge)
                    print (str(arb_yield))

                if arb_yield > 1.02:
                    arbitrage_opportunities.append(arbitrage)

        print ("ARBITRAGE: " + str(arbitrage_opportunities))
        return arbitrage_opportunities






# test = weighted_graph(['USD', 'CAD', 'GBP'])#, 'JPY', 'AUD'])
# arb = test.show_arbitrage_opportunities()
