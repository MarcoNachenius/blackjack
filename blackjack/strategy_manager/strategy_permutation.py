from typing import List
import copy
decision_a = ["0", "1", "2"]
decision_b = ["0", "1", "2", "3"]
decision_c = ["0", "1", "2"]
decision_d = ["0", "1", "2", "3"]
decisions = [decision_a, decision_b, decision_c, decision_d]


def amount_of_possible_permutations(decision_list: List[str]) -> int:
    possible_permutations = 1
    for desc in decision_list:
        possible_permutations *= len(desc)
    return possible_permutations


def produce_next_route_indexes(decision_list: List[List], previous_route_indexes: List[int] = None) -> List[int]:
    total_decisions = len(decision_list)
    if previous_route_indexes == None:
        empty_list = []
        for _ in range(total_decisions):
            empty_list.append(0)
        return empty_list
    next_route = copy.deepcopy(previous_route_indexes)
    route_found = False
    for i in range(total_decisions-1, -1, -1):
        if route_found:
            break
        index_depth = previous_route_indexes[i] +1
        if index_depth < len(decision_list[i]):
            next_route[i] += 1
            route_found = True
        else: 
            next_route[i] = 0
        
    return next_route
        

if __name__ == '__main__':
    index_list = None
    iterations = 5
    for _ in range(amount_of_possible_permutations(decision_list=decisions)):
        index_list = produce_next_route_indexes(decision_list=decisions, previous_route_indexes=index_list)
        print(index_list)
        
# Values starting with index 0
val0 = "000"
val1 = "001"
val2 = "002"
val3 = "010"
val4 = "011"
val5 = "012"
val6 = "020"
val7 = "021"
val8 = "022"
val9 = "030"
val10 = "031"
val11 = "032"
# Values starting with index 1
val12 = "100"
val13 = "101"
val14 = "102"
val15 = "110"
val16 = "111"
val17 = "112"
val18 = "120"
val19 = "121"
val20 = "122"
val21 = "130"
val22 = "131"
val23 = "132"
# Values starting with index 2
val12 = "200"
val13 = "201"
val14 = "202"
val15 = "210"
val16 = "211"
val17 = "212"
val18 = "220"
val19 = "221"
val20 = "222"
val21 = "230"
val22 = "231"
val23 = "232"
