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
    def setUp(self):
        self.blocks_sagrow = self.get_blocks_sagrow()
        self.s3_sagrow = self.get_s3_sagrow()
            
    def test_well_formed_alignment_assertion(self):
        try:
            sagrow = SimAnnealGrow([], dict(), dict())
            print('A')
            self.assertTrue(False, 'Non-well-formed alignment got through')
            print('Z')
        except:
            print('B')
            pass

        print('C')

    def test_null_params(self):
        try:
            sagrow = SimAnnealGrow([], dict(), dict())
            print('a')
        except:
            self.assertTrue(False, 'Null params should get through')
            print('b')

        print('c')
        
    def get_blocks_sagrow(self):
        # used to test block behavior
        return SimAnnealGrow([
            [('a', 'B')],
            [('b', 'A')],
            [('c', 'D'), ('a', 'B')],
            [('c', 'D'), ('e', 'F')],
            [('a', 'X')],
            [('y', 'B')]
        ], {
            'a': {},
            'b': {},
            'c': {},
            'e': {},
            'y': {},
        }, {
            'B': {},
            'A': {},
            'D': {},
            'F': {},
            'X': {},
        })
        
    def test_no_remove_last(self):
        self.assertTrue(self.blocks_sagrow._move_is_valid(0))
        self.blocks_sagrow._make_move(0)
        self.assertFalse(self.blocks_sagrow._move_is_valid(0))
        self.blocks_sagrow._make_move(1)
        self.assertTrue(self.blocks_sagrow._move_is_valid(0))

    def test_non_injective_add(self):
        self.assertTrue(self.blocks_sagrow._move_is_valid(4))
        self.assertTrue(self.blocks_sagrow._move_is_valid(5))
        self.blocks_sagrow._make_move(0)
        self.assertFalse(self.blocks_sagrow._move_is_valid(4))
        self.assertFalse(self.blocks_sagrow._move_is_valid(5))

    def test_add_bookkeeping_update(self):
        self.blocks_sagrow._make_move(0)
        self.assertEqual(self.blocks_sagrow._pair_multiset, {('a', 'B'): 1})
        self.assertEqual(self.blocks_sagrow._forward_mapping, {'a': 'B'})
        self.assertEqual(self.blocks_sagrow._reverse_mapping, {'B': 'a'})
        self.blocks_sagrow._make_move(2)
        self.assertEqual(self.blocks_sagrow._pair_multiset, {('a', 'B'): 2, ('c', 'D'): 1})
        self.assertEqual(self.blocks_sagrow._forward_mapping, {'a': 'B', 'c': 'D'})
        self.assertEqual(self.blocks_sagrow._reverse_mapping, {'B': 'a', 'D': 'c'})
        self.blocks_sagrow._make_move(3)
        self.assertEqual(self.blocks_sagrow._pair_multiset, {('a', 'B'): 2, ('c', 'D'): 2, ('e', 'F'): 1})
        self.assertEqual(self.blocks_sagrow._forward_mapping, {'a': 'B', 'c': 'D', 'e': 'F'})
        self.assertEqual(self.blocks_sagrow._reverse_mapping, {'B': 'a', 'D': 'c', 'F': 'e'})

    def test_remove_bookkeeping_update(self):
        self.blocks_sagrow._make_move(0)
        self.blocks_sagrow._make_move(2)
        self.blocks_sagrow._make_move(3)
        self.assertEqual(self.blocks_sagrow._pair_multiset, {('a', 'B'): 2, ('c', 'D'): 2, ('e', 'F'): 1})
        self.assertEqual(self.blocks_sagrow._forward_mapping, {'a': 'B', 'c': 'D', 'e': 'F'})
        self.assertEqual(self.blocks_sagrow._reverse_mapping, {'B': 'a', 'D': 'c', 'F': 'e'})
        self.blocks_sagrow._make_move(2)
        self.assertEqual(self.blocks_sagrow._pair_multiset, {('a', 'B'): 1, ('c', 'D'): 1, ('e', 'F'): 1})
        self.assertEqual(self.blocks_sagrow._forward_mapping, {'a': 'B', 'c': 'D', 'e': 'F'})
        self.assertEqual(self.blocks_sagrow._reverse_mapping, {'B': 'a', 'D': 'c', 'F': 'e'})
        self.blocks_sagrow._make_move(3)
        self.assertEqual(self.blocks_sagrow._pair_multiset, {('a', 'B'): 1})
        self.assertEqual(self.blocks_sagrow._forward_mapping, {'a': 'B'})
        self.assertEqual(self.blocks_sagrow._reverse_mapping, {'B': 'a'})

    def get_s3_sagrow(self):
        return SimAnnealGrow([
            [('a', 'A'), ('b', 'B')],
            [('c', 'C')],
            [('d', 'D')],
            [('e', 'E')],
        ], {
            'a': {'b', 'e'},
            'b': {'a', 'c', 'd'},
            'c': {'b', 'd'},
            'd': {'b', 'c'},
            'e': {'a'},
        }, {
            'A': {'B'},
            'B': {'A', 'C', 'D', 'E'},
            'C': {'B', 'D', 'E'},
            'D': {'B', 'C'},
            'E': {'B', 'C'},
        }, s3_threshold=0) # set threshold to 0 so all moves are valid
        
    def test_s3_initial(self):
        self.assertEqual(self.s3_sagrow._s3_frac, [0, 0])

    def test_add_s3_update(self):
        self.s3_sagrow._make_move(1)
        self.assertEqual(self.s3_sagrow._s3_frac, [0, 0])
        self.s3_sagrow._make_move(0)
        self.assertEqual(self.s3_sagrow._s3_frac, [2, 2])
        self.s3_sagrow._make_move(2)
        self.assertEqual(self.s3_sagrow._s3_frac, [4, 4])
        self.s3_sagrow._make_move(3)
        self.assertEqual(self.s3_sagrow._s3_frac, [4, 7])

class SimAnnealGrow:
    # blocks are the building block alignments
    def __init__(self, blocks, adj_set1, adj_set2, s3_threshold=1):
        assert all(is_well_formed_alignment(block) for block in blocks)
        assert is_symmetric_adj_set(adj_set1)
        assert is_symmetric_adj_set(adj_set2)
        self._blocks = blocks
        self._adj_set1 = adj_set1
        self._adj_set2 = adj_set2
        self._s3_threshold = s3_threshold
        
        self._pair_multiset = dict()
        self._forward_mapping = dict()
        self._reverse_mapping = dict()
        self._s3_frac = [0, 0]
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

        if is_adding:
            # s3 should be updated before the bookkeeping stuff for efficiency
            self._update_s3_after_add(block_i)
            self._update_block_bookkeeping_after_add(block_i)
        else:
            self._update_block_bookkeeping_after_remove(block_i)

    def _update_block_bookkeeping_after_add(self, block_i):
        block = self._blocks[block_i]
        self._num_used_blocks += 1
                    
        for node1, node2 in block:
            pair = (node1, node2)

            if pair not in self._pair_multiset:
                self._pair_multiset[pair] = 1
                self._forward_mapping[node1] = node2
                self._reverse_mapping[node2] = node1
            else:
                self._pair_multiset[pair] += 1

    def _update_block_bookkeeping_after_remove(self, block_i):
        block = self._blocks[block_i]
        self._num_used_blocks -= 1

        for node1, node2 in block:
            pair = (node1, node2)
            self._pair_multiset[pair] -= 1

            if self._pair_multiset[pair] == 0:
                del self._pair_multiset[pair]
                del self._forward_mapping[node1]
                del self._reverse_mapping[node2]
                
    def _update_s3_after_add(self, block_i):
        block = self._blocks[block_i]
        curr_aligned_pairs = set(self._pair_multiset.keys())

        for node1, node2 in block:
            for curr_node1, curr_node2 in curr_aligned_pairs:
                has_edge1 = node1 in self._adj_set1[curr_node1]
                has_edge2 = node2 in self._adj_set2[curr_node2]

                if has_edge1 and has_edge2:
                    self._s3_frac[0] += 1
                
                if has_edge1 or has_edge2:
                    self._s3_frac[1] += 1

            curr_aligned_pairs.add((node1, node2))

    def _reset(self):
        self._use_block = [False] * len(self._blocks)
        self._num_used_blocks = 0
                    
    def run(self):
        self._make_move(self._get_random_block_i())

    def get_alignment(self):
        return self._alignment

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
    sagrow = SimAnnealGrow(blocks, adj_set1, adj_set2)
    sagrow.run()
    print(sagrow.get_alignment())
