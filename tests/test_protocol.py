import json
from itertools import combinations
import unittest
from unittest.mock import patch
import numpy as np
from thermal_sentinel.data import ROOT,INPUTS,TARGETS,IQ,split,get_profiles
from thermal_sentinel.experiment import condition,features,forward_fill,SCENARIOS,basic,aggregate

class ProtocolTests(unittest.TestCase):
    def test_frozen_profile_isolation(self):
        cfg=json.loads((ROOT/'configs/split.json').read_text())
        ids=[i for group in cfg.values() for i in group]
        self.assertEqual(len(ids),69)
        self.assertEqual(len(set(ids)),69)
        self.assertEqual(split(ids),cfg)
        self.assertTrue(all(not set(a)&set(b) for a,b in combinations(cfg.values(),2)))
        self.assertFalse(set(INPUTS)&set(TARGETS))
        self.assertNotIn('profile_id',INPUTS)
        self.assertNotIn('torque',INPUTS)

    def test_profile_resampling_does_not_bridge_groups(self):
        # Explicit unit-test fixture, not experimental or reported motor data.
        cfg=json.loads((ROOT/'configs/split.json').read_text())
        ids=sorted(i for g in cfg.values() for i in g)
        cols=INPUTS+TARGETS+['profile_id']
        raw=np.zeros((len(ids)*5,len(cols)),dtype=np.float32)
        for k,pid in enumerate(ids):raw[k*5:k*5+5,-1]=pid
        with patch('thermal_sentinel.data.read_data',return_value=(cols,raw)):
            got,data=get_profiles(2)
        self.assertEqual(got,cfg)
        self.assertTrue(all(len(x)==3 for x,y in data.values()))

    def test_no_future_features_or_imputation(self):
        x=np.arange(1260,dtype=float).reshape(180,7)/20
        changed=x.copy();changed[90:]+=1000
        np.testing.assert_array_equal(features(x,10)[:90],features(changed,10)[:90])
        q,active=condition(x,46,'outage',20)
        fill=forward_fill(q,np.zeros(7))
        np.testing.assert_array_equal(fill[60:120,IQ],np.repeat(x[59,IQ],60))
        self.assertEqual(features(x,10,False).shape[1],28)
        self.assertEqual(features(x,10,True).shape[1],44)

    def test_faults_only_change_selected_input(self):
        x=np.ones((180,7))*2
        for case in SCENARIOS:
            q,active=condition(x,46,case,20)
            np.testing.assert_array_equal(q[:,np.arange(7)!=IQ],x[:,np.arange(7)!=IQ])
            self.assertTrue(np.isfinite(forward_fill(q,np.zeros(7))).all())
            if case=='bias':np.testing.assert_array_equal(q[60:,IQ],np.repeat(22.,120))

    def test_metric_values_and_weighting(self):
        y=np.array([1.,2.,3.]);p=np.array([0.,2.,5.])
        m=basic(y,p,np.array([False,False,True]))
        self.assertEqual(m['mae'],1.)
        self.assertAlmostEqual(m['rmse'],np.sqrt(5/3))
        self.assertEqual(m['maxae'],2.)
        self.assertEqual(m['active']['mae'],2.)
        a=aggregate([m,m]);self.assertEqual(a['mae'],m['mae'])

    def test_all_unfavourable_results_preserved(self):
        r=json.loads((ROOT/'reports/reference_full.json').read_text())
        self.assertEqual(len(r['models']),5)
        for m in r['models'].values():
            self.assertEqual(set(m['scenarios']),set(SCENARIOS))
            for q in m['scenarios'].values():
                self.assertEqual(len(q['profiles']),8)
                self.assertTrue(all(0<=c<=1 for c in q['coverage']))
                self.assertGreater(q['interval_width_c'],0)
        self.assertGreater(r['models']['Ridge']['scenarios']['bias']['mae'],r['models']['Ridge_plain']['scenarios']['bias']['mae'])

if __name__=='__main__':unittest.main()
