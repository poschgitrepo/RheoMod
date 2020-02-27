# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:02:55 2020

@author: posch
"""
import numpy as np

class model():
       
        # HOOK
        def hook(SIG_old,dEPS,E, DT):
            dSIG = E * dEPS 
            SIG  = SIG_old + dSIG * DT
            return SIG 
        # KELVIN VOIGT
        def kelvinvoigt(EPS, dEPS, E, ETA, DT):
            SIG = E * EPS + ETA * dEPS
            return SIG 
        # MAXWELL
        def maxwell(SIG, dEPS, E, ETA, DT):
            dSIG = E*dEPS-E/ETA*SIG
            SIG = SIG + dSIG * DT
            return SIG 
        # ZENER
        def zener(SIG,dEPS,EPS_D,EPS,E_1,E_2,ETA,DT):
            dEPS_D=E_2/ETA*(EPS-EPS_D)
            dSIG=E_1*dEPS+E_2*(dEPS-dEPS_D)
            SIG=SIG+dSIG*DT
            EPS_D=EPS_D+dEPS_D*DT
            return SIG,EPS_D
    
        # ELASTIC PLASTIC ISO
        def elsatic_plastic_iso(SIG,dEPS_PL,E,SIG_Y,DT,K,ALPHA): #iso IH
            SIG_TRIAL= SIG+E*dEPS_PL*DT
            if (np.abs(SIG_TRIAL)-(SIG_Y+K*ALPHA))<0:
                SIG=SIG_TRIAL
            else:
                dGAMMA=E/(E+K)*dEPS_PL*np.sign(SIG)
                dEPS_P=dGAMMA*np.sign(SIG)
                dALPHA=np.abs(dEPS_P)
                dSIG=E*(dEPS_PL-dEPS_P)
                ALPHA=ALPHA+dALPHA*DT
                SIG=SIG+dSIG*DT
            return SIG,ALPHA
        # ELASTIC PLASTIC KIN
        def elsatic_plastic_kin(SIG,dEPS_PL,E,SIG_Y,DT,Q,H): #kin ih
            SIG_TRIAL= SIG+E*dEPS_PL*DT
            if (np.abs(SIG_TRIAL-Q)-SIG_Y)<0:
                SIG=SIG_TRIAL
            else:
                dGAMMA=(E/(E+H))*dEPS_PL*np.sign(SIG-Q)
                dEPS_P=dGAMMA*np.sign(SIG-Q)
                dQ=H*dEPS_P
                dSIG=E*(dEPS_PL-dEPS_P)
                Q=Q+dQ*DT
                SIG=SIG+dSIG*DT
                #EPS_P=EPS_P+dEPS_P*DT
            return SIG,Q
        # PERZYNA
        def perzyna(SIG,dEPS,E,ETA,SIG_Y,DT):
            SIG_TRIAL= SIG+E*dEPS*DT
            if (np.abs(SIG_TRIAL)-SIG_Y)<0:
                SIG=SIG_TRIAL
            else:
                dEPS_VP =(np.abs(SIG)-SIG_Y)*np.sign(SIG)/ETA
                dSIG=E*(dEPS-dEPS_VP)
                SIG=SIG+dSIG*DT
            return SIG