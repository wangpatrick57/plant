#!/bin/python3
# start with random seed
# at every step, pick a random seed to flip the bit of (remove if it's in the alignment, add if it's not)
# energy function: number of nodes * s3 ** 2
# disallow moves that send the s3 below the threshold
from all_helpers import *
import sys
import unittest

# blocks are the building block alignments
def seeds_to_blocks(seeds):
    blocks = []

    for sid, nodes1, nodes2 in seeds:
        blocks.append(list(zip(nodes1, nodes2)))

    return blocks

class TestSimAnnealGrow(unittest.TestCase):
    def get_testing_blocks(self):
        return [
            [('a', 'B')],
            [('b', 'A')],
            [('c', 'D'), ('a', 'B')],
            [('c', 'D'), ('e', 'F')],
            [('a', 'X')],
            [('y', 'B')]
        ]
    
    def test_no_remove_last(self):
        sagrow = SimAnnealGrow(self.get_testing_blocks())
        self.assertTrue(sagrow._move_is_valid(0))
        sagrow._make_move(0)
        self.assertFalse(sagrow._move_is_valid(0))
        sagrow._make_move(1)
        self.assertTrue(sagrow._move_is_valid(0))

    def test_non_injective_add(self):
        sagrow = SimAnnealGrow(self.get_testing_blocks())
        self.assertTrue(sagrow._move_is_valid(4))
        self.assertTrue(sagrow._move_is_valid(5))
        sagrow._make_move(0)
        self.assertFalse(sagrow._move_is_valid(4))
        self.assertFalse(sagrow._move_is_valid(5))

    def test_add_bookkeeping_update(self):
        sagrow = SimAnnealGrow(self.get_testing_blocks())
        sagrow._make_move(0)
        self.assertEqual(sagrow._pair_multiset, {('a', 'B'): 1})
        self.assertEqual(sagrow._forward_mapping, {'a': 'B'})
        self.assertEqual(sagrow._reverse_mapping, {'B': 'a'})
        sagrow._make_move(2)
        self.assertEqual(sagrow._pair_multiset, {('a', 'B'): 2, ('c', 'D'): 1})
        self.assertEqual(sagrow._forward_mapping, {'a': 'B', 'c': 'D'})
        self.assertEqual(sagrow._reverse_mapping, {'B': 'a', 'D': 'c'})
        sagrow._make_move(3)
        self.assertEqual(sagrow._pair_multiset, {('a', 'B'): 2, ('c', 'D'): 2, ('e', 'F'): 1})
        self.assertEqual(sagrow._forward_mapping, {'a': 'B', 'c': 'D', 'e': 'F'})
        self.assertEqual(sagrow._reverse_mapping, {'B': 'a', 'D': 'c', 'F': 'e'})

    def test_remove_bookkeeping_update(self):
        sagrow = SimAnnealGrow(self.get_testing_blocks())
        sagrow._make_move(0)
        sagrow._make_move(2)
        sagrow._make_move(3)
        self.assertEqual(sagrow._pair_multiset, {('a', 'B'): 2, ('c', 'D'): 2, ('e', 'F'): 1})
        self.assertEqual(sagrow._forward_mapping, {'a': 'B', 'c': 'D', 'e': 'F'})
        self.assertEqual(sagrow._reverse_mapping, {'B': 'a', 'D': 'c', 'F': 'e'})
        sagrow._make_move(2)
        self.assertEqual(sagrow._pair_multiset, {('a', 'B'): 1, ('c', 'D'): 1, ('e', 'F'): 1})
        self.assertEqual(sagrow._forward_mapping, {'a': 'B', 'c': 'D', 'e': 'F'})
        self.assertEqual(sagrow._reverse_mapping, {'B': 'a', 'D': 'c', 'F': 'e'})
        sagrow._make_move(3)
        self.assertEqual(sagrow._pair_multiset, {('a', 'B'): 1})
        self.assertEqual(sagrow._forward_mapping, {'a': 'B'})
        self.assertEqual(sagrow._reverse_mapping, {'B': 'a'})

class SimAnnealGrow:
    # blocks are the building block alignments
    def __init__(self, blocks):
        assert all(all(len(item) == 2 for item in block) for block in blocks)
        self._blocks = blocks
        self._pair_multiset = dict()
        self._forward_mapping = dict()
        self._reverse_mapping = dict()
        # store numer and denom for s3
        self._reset()

    # returns a valid move (without caring about the energy change)
    def _neighbor(self):
        block_i = self._get_random_block_i()
        
        while not self._move_is_valid(block_i):
            block_i = self._get_random_block_i()

        return block_i

    def _move_is_valid(self, block_i):
        is_adding = not self._use_block[block_i]
        
        # we can't remove the last block
        if self._num_used_blocks == 1 and not is_adding:
            return False

        # we can't make the mapping non-injective
        block = self._blocks[block_i]
        
        for node1, node2 in block:
            if node1 in self._forward_mapping:
                if self._forward_mapping[node1] != node2:
                    return False
                
            if node2 in self._reverse_mapping:
                if self._reverse_mapping[node2] != node1:
                    return False

        return True

    def _get_random_block_i(self):
        return random.randrange(len(self._blocks))
    
    # call this to modify use block in order to do some bookkeeping
    def _make_move(self, block_i):
        assert self._move_is_valid(block_i)

        # modify use block
        is_adding = not self._use_block[block_i]
        self._use_block[block_i] = not self._use_block[block_i]

        # modify bookkeeping data structures
        block = self._blocks[block_i]
        
        if is_adding:
            self._num_used_blocks += 1
            
            for node1, node2 in block:
                pair = (node1, node2)
                
                if pair not in self._pair_multiset:
                    self._pair_multiset[pair] = 0
                    
                self._pair_multiset[pair] += 1
                self._forward_mapping[node1] = node2
                self._reverse_mapping[node2] = node1
        else:
            self._num_used_blocks -= 1

            for node1, node2 in block:
                pair = (node1, node2)
                self._pair_multiset[pair] -= 1

                if self._pair_multiset[pair] == 0:
                    del self._pair_multiset[pair]
                    del self._forward_mapping[node1]
                    del self._reverse_mapping[node2]

    def _reset(self):
        self._use_block = [False] * len(self._blocks)
        self._num_used_blocks = 0
                    
    def run(self):
        self._make_move(self._get_random_block_i())

    def get_alignment(self):
        alignment = []

        for use_block, block in zip(self._use_block, self._blocks):
            if use_block:
                alignment.extend(block)

        return alignment

if __name__ == '__main__':
    unittest.main()
    quit()
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    algo = sys.argv[3]
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    seeds_path = get_seeds_path(gtag1, gtag2, algo=algo, prox=1, target_num_matching=1)
    seeds = read_in_seeds(seeds_path)
    blocks = seeds_to_blocks(seeds)
    sagrow = SimAnnealGrow(blocks)
    sagrow.run()
    print(sagrow.get_alignment())
