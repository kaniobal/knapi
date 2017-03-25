import json
import warnings
import math

from __builtin__ import float
from numpy import zeros

class Node:
    """Graph search node representation for Branch and Bound"""
    def __init__(self, level, value, weight, bound, in_knapsack):
        self.level = level
        self.value = value
        self.weight = weight
        self.bound = bound
        self.in_knapsack = in_knapsack

    def __str__(self):
        return 'Node: ' + \
               ' level: ' + str(self.level) + \
               '\n value: ' + str(self.value) + \
               '\n weight: ' + str(self.weight) + \
               '\n bound: ' + str(self.bound) + \
               '\n items in knapsack: ' + str(self.in_knapsack)

    def __repr__(self):
        return 'Node: ' + \
               ' level: ' + str(self.level) + \
               '\n value: ' + str(self.value) + \
               '\n weight: ' + str(self.weight) + \
               '\n bound: ' + str(self.bound) + \
               '\n items in knapsack: ' + str(self.in_knapsack)


class KnapsackSolver:
    """Solves knapsack packing problem"""
    def __init__(self):
        self.knapsack = []
        self.v_tot = 0
        self.w_tot = 0
        self.capacity = 0
        self.items = []
        self.num_items = 0
        self.weights = []
        self.values = []

    def load_data_from_file(self, filename):
        with open(filename) as json_data:
            raw_data = json.load(json_data)

        self.init_attrs_from_data(raw_data)

    def load_data_from_json_string(self, json_string):
        raw_data = json.loads(json_string)

        self.init_attrs_from_data(raw_data)

    def init_attrs_from_data(self, raw_data):
        self.capacity = raw_data['capacity']
        self.items = sorted(raw_data['items'], key=lambda item: float('inf') if item['value'] == 0 else float(item['weight']) / float(item['value']))
        self.num_items = len(raw_data['items'])
        if raw_data['num_items'] != self.num_items:
            warnings.warn('Declared number of items is not the actual number of supplied items')

    def extract_weights_and_values(self):
        """Translates items dict into weights and values lists preserving indices"""
        self.weights = [None] * (self.num_items + 1)
        self.values = [None] * (self.num_items + 1)
        for item in self.items:
            self.weights[item['index'] + 1] = item['weight']
            self.values[item['index'] + 1] = item['value']

    def solve(self, algo='a'):
        self.knapsack = []

        algos_shortnames = {
            'bab': 'branch and bound',
            'dp': 'dynamic programming',
            'ghq': 'greedy heuristic',
            'a': 'auto',
        }

        if len(algo) < 5:
            algo = algos_shortnames[algo]

        if algo == 'branch and bound':
            self.branch_and_bound_solve()
        elif algo == 'dynamic programming':
            self.dynamic_programming_solve()
        elif algo == 'greedy heuristic':
            self.greedy_heuristic_quasisolve()
        elif algo == 'auto':
            if self.num_items < 100:
                self.dynamic_programming_solve()
            else:
                self.branch_and_bound_solve()

    def dynamic_programming_solve(self):
        # more handy data representation
        self.extract_weights_and_values()

        # init best value matrix
        mat = zeros((self.num_items + 1, self.capacity + 1), int)

        for i in xrange(1, self.num_items + 1):
            for j in xrange(0, self.capacity + 1):
                
                if self.weights[i] > j:
                    mat[i][j] = mat[i - 1][j]
                else:
                    mat[i][j] = max(mat[i - 1][j], mat[i - 1][j - self.weights[i]] + self.values[i])

        i = self.num_items
        j = self.capacity
        self.v_tot = mat[i][j]
        while mat[i][j] > 0 and i >= 0:
            
            if mat[i][j] > mat[i - 1][j]:
                self.knapsack.append({
                    'index': i - 1,  # originally shifted by 1 by extractWeightsAndValues
                    'value': self.values[i],
                    'weight': self.weights[i],
                })
                self.w_tot += self.weights[i]
                j -= self.weights[i]
                i -= 1
            else:
                i -= 1

    def calculate_upper_bound(self, node):
        if node.weight > self.capacity:
            return 0
        else:
            bound = node.value
            w_tot = node.weight
            item_index = node.level
            while item_index < self.num_items and w_tot + self.items[item_index]['weight'] <= self.capacity:
                bound += self.items[item_index]['value']
                w_tot += self.items[item_index]['weight']
                item_index += 1

            if item_index < self.num_items:
                bound += float(self.capacity - w_tot)/self.items[item_index]['weight'] * self.items[item_index]['value']

            return bound

    def branch_and_bound_solve(self):

        # init
        root_node = Node(0, 0, 0, 0, [])
        root_node.bound = self.calculate_upper_bound(root_node)
        queue = [root_node]

        while len(queue) > 0:
            cur_node = queue.pop()

            # no prospects here
            if cur_node.bound <= self.v_tot:
                continue

            cur_item_index = cur_node.level
            cur_lvl = cur_item_index + 1

            added_option = Node(cur_lvl, cur_node.value + self.items[cur_item_index]['value'], cur_node.weight + self.items[cur_item_index]['weight'], cur_node.bound, cur_node.in_knapsack[:])
            added_option.in_knapsack.append(self.items[cur_item_index])
            if added_option.weight <= self.capacity:
                if added_option.value > self.v_tot:
                    self.v_tot = added_option.value
                    self.w_tot = added_option.weight
                    self.knapsack = added_option.in_knapsack

                if added_option.bound > self.v_tot:
                    
                    queue.append(added_option)

            omitted_option = Node(cur_lvl, cur_node.value, cur_node.weight, 0, cur_node.in_knapsack[:])
            omitted_option.bound = self.calculate_upper_bound(omitted_option)
            if added_option.bound > self.v_tot:
                queue.append(omitted_option)

            queue = sorted(queue, key=lambda node: node.bound)

    def greedy_heuristic_quasisolve(self):
        for item in self.items:
            if self.w_tot + item['weight'] <= self.capacity:
                self.w_tot += item['weight']
                self.v_tot += item['value']
                self.knapsack.append(item)
