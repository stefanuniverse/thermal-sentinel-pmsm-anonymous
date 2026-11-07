"""Use author MIT TNNCell and DiffEqLayer, with a leakage-controlled harness."""
import hashlib
import json
import linecache
import math
import sys
import types
from typing import List, Tuple
import numpy as np
from .data import ROOT, INPUTS, TARGETS, SEED

import torch
from torch import Tensor, nn

from .third_party.thermal_nn_cell import TNNCell, DiffEqLayer

def upstream():
    return TNNCell, DiffEqLayer

class SignedAblation(nn.Module):
    """Keep topology, capacitance and solver; remove positivity of edge and heat functions."""
    def __init__(self, base):
        super().__init__()
        self.caps=base.caps
        self.edge=base.conductance_net[0]
        self.ploss=base.ploss
        self.adj_mat=base.adj_mat
        self.temp_idcs=base.temp_idcs
        self.sample_time=base.sample_time

    def forward(self,inp:Tensor,state:Tensor)->Tuple[Tensor,Tensor]:
        temps=torch.cat([state,inp[:,self.temp_idcs]],dim=1)
        s=torch.cat([inp,state],dim=1)
        conducts=.5+.25*self.edge(s)  # linearization of sigmoid around zero, allowed negative
        flow=torch.sum((temps.unsqueeze(1)-state.unsqueeze(-1))*conducts[:,self.adj_mat],dim=-1)
        out=state+self.sample_time*torch.exp(self.caps)*(flow+self.ploss(s))
        return state,torch.clip(out,-1,5)

def fit_tnn(data,sets,dt,epochs,signed):
    torch.set_num_threads(1)
    torch.manual_seed(SEED)
    cell,layer=upstream()
    norm=np.max(np.abs(np.concatenate([data[i][0] for i in sets["train"]])),axis=0)
    norm=np.maximum(norm,1e-6)
    norm[:2]=200
    def xform(x):
        z=x/norm
        return np.column_stack([z,np.hypot(z[:,5],z[:,6]),np.hypot(z[:,2],z[:,3])]).astype(np.float32)
    def packed(ids):
        n=max(len(data[i][0]) for i in ids)
        x=np.zeros((n,len(ids),9),np.float32)
        y=np.zeros((n,len(ids),4),np.float32)
        mask=np.zeros((n,len(ids)),bool)
        for j,i in enumerate(ids):
            xi,yi=data[i]
            t=len(xi)
            x[:t,j]=xform(xi)
            x[t:,j]=x[t-1,j]
            y[:t,j]=yi/200
            mask[:t,j]=True
        return torch.from_numpy(x),torch.from_numpy(y),torch.from_numpy(mask)
    def factory():
        base=cell()
        base.sample_time=dt
        return SignedAblation(base) if signed else base
    model=torch.jit.script(layer(factory))
    optimizer=torch.optim.Adam(model.parameters(),lr=.004)
    tx,ty,tm=packed(sets["train"])
    vx,vy,vm=packed(sets["validation"])
    def initial(x):
        return x[0,:,:2].mean(dim=-1,keepdim=True).expand(-1,4).contiguous()
    best=float("inf")
    best_epoch=0
    state=None
    hist=[]
    for epoch in range(epochs):
        model.train()
        hidden=initial(tx)
        for start in range(0,len(tx),128):
            end=start+128
            optimizer.zero_grad(set_to_none=True)
            pred,hidden=model(tx[start:end],hidden.detach())
            diff=pred-ty[start:end]
            m=tm[start:end]
            loss=(diff.square()*m[:,:,None]).sum()/(4*m.sum())
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
            optimizer.step()
        model.eval()
        with torch.no_grad():
            p,_=model(vx,initial(vx))
            val=float(((p[:,:,0]-vy[:,:,0]).abs()*vm).sum()/vm.sum())*200
        hist.append(val)
        print(f"{'signed' if signed else 'author'} epoch {epoch+1}/{epochs} validation PM MAE {val:.3f}",flush=True)
        if math.isfinite(val) and val<best:
            best=val
            best_epoch=epoch+1
            state={k:v.detach().clone() for k,v in model.state_dict().items()}
    assert state is not None
    model.load_state_dict(state)
    model.eval()
    filename="tnn-signed.pt" if signed else "tnn-author.pt"
    model.save(str(ROOT/"results"/filename))
    def predict(x):
        z=torch.from_numpy(xform(x))[:,None,:]
        with torch.no_grad():
            p,_=model(z,initial(z))
        return p[:,0,0].numpy()*200
    return predict,sum(p.numel() for p in model.parameters()),dict(best_epoch=best_epoch,validation_pm_mae_c=hist,
        initialization="mean of measured ambient and coolant, copied to four states",
        training_max_abs=norm.tolist(),pytorch=torch.__version__,actual_step_seconds=dt)
