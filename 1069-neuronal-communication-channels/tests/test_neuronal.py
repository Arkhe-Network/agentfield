import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from neuronal_channels import Neuron, Synapse, GapJunction, set_current_time

class TestNeuronalChannels(unittest.TestCase):
    def test_neuron_init(self):
        n = Neuron(1, theosis=0.8)
        self.assertEqual(n.id, 1)
        self.assertEqual(n.theosis, 0.8)

    def test_synapse_plasticity(self):
        n1 = Neuron(1, theosis=0.8)
        n2 = Neuron(2, theosis=0.5)
        syn = Synapse(n1, n2, w=1.0)
        n1.add_synapse(syn)

        initial_w = syn.w
        set_current_time(0.0)
        for i in range(10):
            n1.update(0.1, external_current=100.0)
        self.assertTrue(syn.w > initial_w)

if __name__ == '__main__':
    unittest.main()
