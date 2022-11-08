#!/bin/python3
# start with random seed
# at every step, pick a random seed to flip the bit of (remove if it's in the alignment, add if it's not)
# energy function: number of nodes * s3 ** 2
# disallow moves that send the s3 below the threshold
from all_helpers import *
import sys
import copy
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
        self.blank_sagrow = self.get_blank_sagrow()
        
    def test_null_params(self):
        try:
            sagrow = SimAnnealGrow([], dict(), dict())
            found_error = False
        except:
            found_error = True

        self.assertFalse(found_error, 'Null params didn\'t get through')
        
    def test_well_formed_alignment_assertion(self):
        try:
            sagrow = SimAnnealGrow([('a', 'b'), ('a', 'b', 'c')], dict(), dict())
            found_error = False
        except:
            found_error = True

        self.assertTrue(found_error, 'Non-well-formed alignment got through')

    def test_symmetric_adj_set_assertion(self):
        try:
            sagrow = SimAnnealGrow([], {'a': {'b'}}, dict())
            found_error = False
        except:
            found_error = True

        self.assertTrue(found_error, 'Asymmetric adj_set got through')

        try:
            sagrow = SimAnnealGrow([], dict(), {'a': {'b', 'c'}, 'b': {'c'}, 'c': {'a'}})
            found_error = False
        except:
            found_error = True

        self.assertTrue(found_error, 'Asymmetric adj_set got through')
        
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
        }, s3_threshold=None) # set threshold to None so all moves are valid
        
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
        }, s3_threshold=None) # set threshold to None so all moves are valid
        
    def test_s3_initial(self):
        self.assertEqual(self.s3_sagrow._s3_frac, [0, 0])

    def test_add_s3_update(self):
        self.s3_sagrow._make_move(0)
        self.assertEqual(self.s3_sagrow._s3_frac, [1, 1])
        self.s3_sagrow._make_move(1)
        self.assertEqual(self.s3_sagrow._s3_frac, [2, 2])
        self.s3_sagrow._make_move(2)
        self.assertEqual(self.s3_sagrow._s3_frac, [4, 4])
        self.s3_sagrow._make_move(3)
        self.assertEqual(self.s3_sagrow._s3_frac, [4, 7])

    def test_add_multiple_s3_update(self):
        self.s3_sagrow._make_move(1)
        self.s3_sagrow._make_move(2)
        self.s3_sagrow._make_move(3)
        self.assertEqual(self.s3_sagrow._s3_frac, [1, 2])
        self.s3_sagrow._make_move(0)
        self.assertEqual(self.s3_sagrow._s3_frac, [4, 7])

    def test_remove_s3_update(self):
        self.s3_sagrow._make_move(0)
        self.s3_sagrow._make_move(1)
        self.s3_sagrow._make_move(2)
        self.s3_sagrow._make_move(3)
        self.assertEqual(self.s3_sagrow._s3_frac, [4, 7])
        self.s3_sagrow._make_move(2)
        self.assertEqual(self.s3_sagrow._s3_frac, [2, 5])
        self.s3_sagrow._make_move(3)
        self.assertEqual(self.s3_sagrow._s3_frac, [2, 2])
        self.s3_sagrow._make_move(1)
        self.assertEqual(self.s3_sagrow._s3_frac, [1, 1])

    def test_remove_multiple_s3_update(self):
        self.s3_sagrow._make_move(0)
        self.s3_sagrow._make_move(1)
        self.s3_sagrow._make_move(2)
        self.s3_sagrow._make_move(3)
        self.assertEqual(self.s3_sagrow._s3_frac, [4, 7])
        self.s3_sagrow._make_move(0)
        self.assertEqual(self.s3_sagrow._s3_frac, [1, 2])

    def test_s3_frac_denom_zero(self):
        self.s3_sagrow._s3_threshold = None
        self.assertTrue(self.s3_sagrow._move_is_valid(2))
        self.s3_sagrow._make_move(2)
        self.assertTrue(self.s3_sagrow._move_is_valid(3))
        self.s3_sagrow._s3_threshold = 0
        self.assertFalse(self.s3_sagrow._move_is_valid(3))
        
    def test_s3_threshold_adding(self):
        self.s3_sagrow._s3_threshold = 1.0
        self.assertTrue(self.s3_sagrow._move_is_valid(0))
        self.s3_sagrow._make_move(0)
        self.assertTrue(self.s3_sagrow._move_is_valid(1))
        self.s3_sagrow._make_move(1)
        self.assertTrue(self.s3_sagrow._move_is_valid(2))
        self.s3_sagrow._make_move(2)
        self.assertFalse(self.s3_sagrow._move_is_valid(3))
        self.s3_sagrow._s3_threshold = 0.55
        self.assertTrue(self.s3_sagrow._move_is_valid(3))
        self.s3_sagrow._s3_threshold = 0.6
        self.assertFalse(self.s3_sagrow._move_is_valid(3))

    def get_blank_sagrow(self):
        return SimAnnealGrow(list(), dict(), dict(), s3_threshold=None)
        
    def test_p(self):
        self.assertEqual(self.blank_sagrow._temperature, 1)
        self.assertEqual(self.blank_sagrow._P(5, 3), 1)
        self.assertEqual(self.blank_sagrow._P(3, 5), math.exp(-2))
        self.blank_sagrow._temperature = 0.5
        self.assertEqual(self.blank_sagrow._P(3, 5), math.exp(-4))

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

    def _temperature(self, k, k_max):
        return 1 - (k + 1) / k_max
    
    def _P(self, e, e_new):
        if e_new < e:
            return 1.0
        else:
            return math.exp(-(e_new - e) / self._temperature)

    @staticmethod
    def s3_frac_to_s3(s3_frac):
        if s3_frac[1] == 0:
            return None
        else:
            return s3_frac[0] / s3_frac[1]
    
    def _move_is_valid(self, block_i):
        is_adding = not self._use_block[block_i]
        block = self._blocks[block_i]
        
        # we can't remove the last block
        if not is_adding and self._num_used_blocks == 1:
            return False

        # we can't make the mapping non-injective with an add
        if is_adding:
            for node1, node2 in block:
                if node1 in self._forward_mapping:
                    if self._forward_mapping[node1] != node2:
                        return False

                if node2 in self._reverse_mapping:
                    if self._reverse_mapping[node2] != node1:
                        return False

        # we can't go below the threshold
        updated_s3_frac = self._get_updated_s3_frac(block_i, is_adding)
        updated_s3 = SimAnnealGrow.s3_frac_to_s3(updated_s3_frac)
        
        # even the first move has to have good enough s3, so we don't have a special case for that. moves add blocks at a time not nodes, so we don't treat the first move differently
        if self._s3_threshold == None:
            pass # if the threshold is None, we'll even allow moves that give undefined s3 scores
        else:
            if updated_s3 == None or updated_s3 < self._s3_threshold:
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

        # s3 should be updated before the bookkeeping stuff
        if is_adding:
            self._s3_frac = self._get_updated_s3_frac(block_i, True)
            self._update_block_bookkeeping_after_add(block_i)
        else:
            self._s3_frac = self._get_updated_s3_frac(block_i, False)
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
                
    def _get_updated_s3_frac(self, block_i, is_adding):
        # this function does not update any internal fields
        block = self._blocks[block_i]
        curr_aligned_pairs = set(self._pair_multiset.keys())
        delta = 1 if is_adding else -1
        updated_s3_frac = copy.copy(self._s3_frac)

        for node1, node2 in block:
            for curr_node1, curr_node2 in curr_aligned_pairs:
                has_edge1 = node1 in self._adj_set1[curr_node1]
                has_edge2 = node2 in self._adj_set2[curr_node2]

                if has_edge1 and has_edge2:
                    updated_s3_frac[0] += delta
                
                if has_edge1 or has_edge2:
                    updated_s3_frac[1] += delta

            if is_adding:
                curr_aligned_pairs.add((node1, node2))
            else:
                curr_aligned_pairs.remove((node1, node2))

        return updated_s3_frac

    def _reset(self):
        self._use_block = [False] * len(self._blocks)
        self._num_used_blocks = 0
        self._temperature = 1
                    
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
