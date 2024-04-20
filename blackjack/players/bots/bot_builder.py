from blackjack.players.bots.strategist_abc import Strategist

class BotBuilder(object):
    
    @classmethod
    def return_random_player(cls, player_name: str = "Random Strategist") -> Strategist:
        """
        Returns a Strategist bot with randomly generated strategy matrixes
        """
        random_player = Strategist(player_name=player_name)
        
        # Generate random matrixes
        hard_total_matrix = random_player.hard_total_strategy.generate_random_permutation()
        soft_total_matrix = random_player.soft_total_strategy.generate_random_permutation()
        split_total_matrix = random_player.split_pair_strategy.generate_random_permutation()
        
        # Set strategy matrixes
        random_player.hard_total_strategy.set_strategy_matrix(hard_total_matrix)
        random_player.soft_total_strategy.set_strategy_matrix(soft_total_matrix)
        random_player.split_pair_strategy.set_strategy_matrix(split_total_matrix)
        
        return random_player
    
    @classmethod
    def return_next_permutation_player(cls, player: Strategist) -> Strategist:
        """
        Returns a Strategist bot with with all strategy matrixes moved up a step.
        """
        new_permutation_player = Strategist(player_name="Random Strategist")
        
        # Generate next matrix permutations
        hard_total_matrix = player.hard_total_strategy.generate_next_permutation(player.hard_total_strategy.get_strategy_matrix())
        soft_total_matrix = player.soft_total_strategy.generate_next_permutation(player.soft_total_strategy.get_strategy_matrix())
        split_total_matrix = player.split_pair_strategy.generate_next_permutation(player.split_pair_strategy.get_strategy_matrix())
        
        # Set strategy matrixes
        new_permutation_player.hard_total_strategy.set_strategy_matrix(hard_total_matrix)
        new_permutation_player.soft_total_strategy.set_strategy_matrix(soft_total_matrix)
        new_permutation_player.split_pair_strategy.set_strategy_matrix(split_total_matrix)
        
        return new_permutation_player