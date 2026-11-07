import unittest
import numpy as np
import torch
from thermal_sentinel.third_party.thermal_nn_cell import TNNCell,DiffEqLayer
from thermal_sentinel.lptn import predict

class ModelTests(unittest.TestCase):
    def test_author_cell_shapes_finite_and_parameter_count(self):
        torch.manual_seed(260711)
        cell=TNNCell()
        self.assertEqual(sum(p.numel() for p in cell.parameters()),506)
        x=torch.zeros(3,9);hidden=torch.ones(3,4)*.2
        out,state=cell(x,hidden)
        self.assertEqual(out.shape,(3,4))
        self.assertTrue(torch.isfinite(state).all())
        torch.testing.assert_close(out,hidden)
        layer=torch.jit.script(DiffEqLayer(TNNCell))
        seq,last=layer(torch.zeros(5,3,9),hidden)
        self.assertEqual(seq.shape,(5,3,4))
        self.assertTrue(torch.isfinite(last).all())

    def test_lptn_boundary_initialization_and_scale_invariance(self):
        x=np.zeros((20,7));x[:,0]=20;x[:,1]=40
        parameters=np.array([.02,.03,.001,0.,0.]);c=2
        a=predict(x,parameters/c)
        self.assertEqual(a[0],30)
        np.testing.assert_allclose(a,predict(x,(17*parameters)/(17*c)))
        self.assertTrue(np.isfinite(a).all())

if __name__=='__main__':unittest.main()
