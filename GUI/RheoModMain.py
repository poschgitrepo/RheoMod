#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
# 
# +============================================================================
# | PROGRAM NAME: WMD MODEL DESIGNER    -------- by B. Eng. A. R. Schultz
# +============================================================================
# | PROGRAM DESCRIPTION:                                                                           
# | --------------------
# |                                                                                                
# |                                                                                                
# +============================================================================
# |                                                                                              
# | ARGUMENTS:                                                                                   
# | +----+---------------------------------------------------------------------
# | | ## | DESCRIPTION                                                          
# | +----+---------------------------------------------------------------------
# | |    |                                                                     
# | +----+---------------------------------------------------------------------
# |                                                                            
# +============================================================================
# |                                                                                                
# | CHANGE LOG:                                                                                    
# | +-------+------------+-----+-----------------------------------------------
# | |VERSION|    DATE    | TRI | DESCRIPTION                                                     
# | +-------+------------+-----+-----------------------------------------------
# | |  2.0  | 27.02.2020 | ARS | 2nd version                                                     
# | +-------+------------+-----------------------------------------------------
# |                                                                                                
# +============================================================================
# |                                                                                                
# | DEPENDENCIES:                                                                                  
# | +--------------------------------------------------------------------------
# | |
# | +--------------------------------------------------------------------------
# |                                                                                                
# +============================================================================
'''
# =============================================================================
# Import Section
# =============================================================================

from PyQt5 import QtWidgets,uic
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import numpy as np
import sys


# =============================================================================
# Import Rheological Moodels 
# =============================================================================
from RheoModModel import model    
# =============================================================================
# GUI CLASS UI
# =============================================================================

class Ui(QtWidgets.QDialog):
    # Init UI CLASS
    def __init__(self):
        super(Ui, self).__init__()
        # ====================================================================
        # Load UI XML DATA  
        # ====================================================================
        uic.loadUi('RheoModGui.ui', self)
        # ====================================================================
        # Connect Buttons with the Plot functions      
        # ====================================================================    
        self.PLOT_LOADING.clicked.connect(self.set_loading)
        self.PLOT_MODEL.clicked.connect(self.plot_model)
        
        
    # =========================================================================
    # Plot Funktion for all Plots in the GUI        
    # =========================================================================
        
    def plot_in_gui(self,x,y,plot_label,x_label,y_label,
                    Title,WINDOW,Plot_on,grid='on',number_of_plots=1):
        fig=Figure()
        model = fig.add_subplot(111)
        for i in range(0,number_of_plots):
            if Plot_on[i]==True:
                model.plot(x,y[:,i+1],'-' , label=plot_label[i])
        model.set_xlabel(x_label)
        model.set_ylabel(y_label)
        model.grid(grid)
        model.legend()
        model.set_title(Title)
        # ====================================================================
        # PLOT WINDOW SETTING FOR LOADING PLOTS   
        # ==================================================================== 
        if WINDOW=='LOADING':
            try:
             self.PLOT_BOX_LOADING.removeWidget(self.canvas_LOADING)
             self.canvas_LOADING.close()
             self.PLOT_BOX_LOADING.removeWidget(self.toolbar_LOADING)
             self.toolbar_LOADING.close()
            except AttributeError:
             print ('NO CAVAS FOUND')
            self.canvas_LOADING = FigureCanvas(fig)
            self.PLOT_BOX_LOADING.addWidget(self.canvas_LOADING)
            self.canvas_LOADING.draw()
            self.toolbar_LOADING = NavigationToolbar(self.canvas_LOADING, 
                self.PLOT_WIN_LOADING, coordinates=True)
            self.TOOL_BOX_LOADING.addWidget(self.toolbar_LOADING)
        # ====================================================================
        # PLOT WINDOW SETTING FOR STRESS TIME PLOTS   
        # ====================================================================    
        if WINDOW=='STRESS_TIME':
            try:
             self.PLOT_BOX_STRESS_TIME.removeWidget(self.canvas_STRESS_TIME)
             self.canvas_STRESS_TIME.close()
             self.PLOT_BOX_STRESS_TIME.removeWidget(self.toolbar_STRESS_TIME)
             self.toolbar_STRESS_TIME.close()
            except AttributeError:
             print ('NO CAVAS FOUND')
            self.canvas_STRESS_TIME = FigureCanvas(fig)
            self.PLOT_BOX_STRESS_TIME.addWidget(self.canvas_STRESS_TIME)
            self.canvas_STRESS_TIME.draw()
            self.toolbar_STRESS_TIME = NavigationToolbar(self.canvas_STRESS_TIME, 
                self.PLOT_WIN_STRESS_TIME, coordinates=True)
            self.TOOL_BOX_STRESS_TIME.addWidget(self.toolbar_STRESS_TIME)  
        # ====================================================================
        # PLOT WINDOW SETTING FOR STRESS STRAIN PLOTS   
        # ====================================================================    
        if WINDOW=='STRESS_STRAIN':
            try:
             self.PLOT_BOX_STRESS_STRAIN.removeWidget(self.canvas_STRESS_STRAIN)
             self.canvas_STRESS_STRAIN.close()
             self.PLOT_BOX_STRESS_STRAIN.removeWidget(self.toolbar_STRESS_STRAIN)
             self.toolbar_STRESS_STRAIN.close()
            except AttributeError:
             print ('NO CAVAS FOUND')
            self.canvas_STRESS_STRAIN = FigureCanvas(fig)
            self.PLOT_BOX_STRESS_STRAIN.addWidget(self.canvas_STRESS_STRAIN)
            self.canvas_STRESS_STRAIN.draw()
            self.toolbar_STRESS_STRAIN = NavigationToolbar(self.canvas_STRESS_STRAIN, 
                self.PLOT_WIN_STRESS_STRAIN, coordinates=True)
            self.TOOL_BOX_STRESS_STRAIN.addWidget(self.toolbar_STRESS_STRAIN)
        
        
    # =========================================================================
    #  Loading       
    # =========================================================================
    def set_loading(self):
        try:
            # Init VAriabels
            Loadingtitle = ([''])
            Plot_on      = ([True])
            # GUI IMPUT
            sr   = self.VAL_STRAIN.value()
            srh  = self.VAL_STRAIN_2.value()
            tr   = self.VAL_TIME.value()
            trh  = self.VAL_TIME_HIGH_STRAIN.value()
            dt   = self.VAL_DT.value()
            st   = self.VAL_TIME_STRESS.value()
            hold = self.VAL_TIME_RELAX.value()
            jump = self.JUMP_STRESS_RELAX.value()
            jump_2 = self.JUPMS_DIFFERENT_STRESS.value()
            
            # ================================================================
            #  + STRESS           
            # ================================================================
            if self.CB_LOAD_POS_STRESS.isChecked()==True:
                Loadingtitle[0]='ONLY STRESS'         
                self.fdEPST=np.array([[sr, sr,] , 
                         [0.00 , tr]])
            # ================================================================
            #  + STRESS  | - STRESS         
            # ================================================================    
            if self.CB_LOAD_POS_NEG_STRESS.isChecked()==True:
                Loadingtitle[0]='HALF TIME POS OTHER NEG STRESS'
                self.fdEPST=np.array([[sr, sr,-(sr),-(sr)] , 
                         [0.00 ,tr/2,tr/2+0.1, tr]])
            # ================================================================
            #  + STRESS CICLE          
            # ================================================================
            if self.CB_LOAD_STRESS_CICLE.isChecked()==True:
                Loadingtitle[0]='STRESS CICLE'
                self.fdEPST=np.array([[sr , sr,-(sr),-(sr),(sr),(sr)] , 
                         [0.00 , tr/4,tr/4+0.1,tr-tr/4,tr-tr/4+0.1,tr]])
            # ================================================================
            #  + STRESS RELAX CICLE          
            # ================================================================ 
            if self.CB_LOAD_STRESS_RELAX_CICLE.isChecked() == True:                
                Loadingtitle[0]='STRESS RELAX CICLE'
                K=1 
                time=(st+hold)*jump*2
                self.VAL_TIME.setValue(time)
                self.fdEPST=np.zeros((2,int(jump*8)))
                self.fdEPST[:,0]=sr,0
                for i in range (0,int(jump)):
                    t=time/(jump*2)*i
                    self.fdEPST[:,K]=sr,t+st
                    self.fdEPST[:,K+1]=0,t+st+dt
                    self.fdEPST[:,K+2]=0,t+st+hold
                    self.fdEPST[:,K+3]=sr,t+st+hold+dt
                    if i==(int(jump-1)):
                        self.fdEPST[:,K+3]=-sr,t+st+hold+dt
                    K=K+4    
                for i in range (int(jump),int(jump)*2):
                    t=time/(jump*2)*i
                    self.fdEPST[:,K]=-sr,t+st
                    self.fdEPST[:,K+1]=0,t+st+dt
                    self.fdEPST[:,K+2]=0,t+st+hold
                    if i<(jump*2-1):
                            self.fdEPST[:,K+3]=-sr,t+st+hold+dt
                    K=K+4                         
            # ================================================================
            #  + STRESS RELAX      
            # ================================================================ 
            if self.CB_LOAD_STRESS_RELAX.isChecked() == True:
                Loadingtitle[0]='STRESS RELAX'
                K=1 
                time=(st+hold)*jump
                self.VAL_TIME.setValue(time)
                self.fdEPST=np.zeros((2,int(jump*4+1)))
                self.fdEPST[:,0]=sr,0
                for i in range (0,int(jump)):
                    t=time/(jump)*i
                    self.fdEPST[:,K]=sr,t+st
                    self.fdEPST[:,K+1]=0,t+st+dt
                    self.fdEPST[:,K+2]=0,t+st+hold
                    self.fdEPST[:,K+3]=sr,t+st+hold+dt
                    K=K+4
            # ================================================================
            #  + STRESS HIGH STRESS     
            # ================================================================         
            if self.CB_LOAD_STRESS_HIGH_STRESS.isChecked()==True:
                Loadingtitle[0]='DIFFERENT STRESS'
                K=0
                self.fdEPST=np.zeros((2,int(jump_2*4+2)))
                self.fdEPST[:,0]=sr,0
                for i in range(1,int(jump_2+1)):          
                    self.fdEPST[:,K]=sr,i*tr/(jump_2+1)
                    self.fdEPST[:,K+1]=srh,i*tr/(jump_2+1)+0.1
                    self.fdEPST[:,K+2]=srh,i*tr/(jump_2+1)+trh
                    self.fdEPST[:,K+3]=sr,i*tr/(jump_2+1)+trh+0.1
                    K=K+4
                self.fdEPST[:,int(jump_2*4+1)]=sr,tr
            # ================================================================
            #  generate Data for Loading Plot  
            # ================================================================ 
            self.NCYCLES =int(self.VAL_TIME.value()/self.VAL_DT.value())
            DATA=np.zeros((self.NCYCLES,2),dtype=float)
            T= 0.
            EPS=0.               
            for i in range(1,self.NCYCLES):
                dEPS   = np.interp(T,self.fdEPST[1,:],self.fdEPST[0,:])
                EPS = EPS + dEPS * self.VAL_DT.value()
                T=T+self.VAL_DT.value()
                DATA[i,0]=T
                DATA[i,1]=EPS 
            print    
            self.plot_in_gui(DATA[:,0],DATA,Loadingtitle,
                             'Time [sec]','$\epsilon$ [mm]',
                             'Loading','LOADING',Plot_on)    
        except AttributeError:
            print('no loding')
            
    # =========================================================================
    # PLOT RESULTS                 
    # =========================================================================
     
    def plot_model(self):
        
        # INIT ALL VARIABLES
        self.DATA=np.zeros((self.NCYCLES,15),dtype=float)
        number_of_plots,SIG_HOOK,T,EPS,SIG_NEO_HOOK,SIG_MAXWELL   = 0,0,0,0,0,0
        SIG_KELVIN_VOIGT,SIG_ZENER,EPS_D_ZENER,models,SIG_PERZYNA = 0,0,0,0,0
        SIG_ELASTIC_PLASTIC_ISO,ALPHA_ELASTIC_PLASTIC_ISO         = 0,0
        SIG_ELASTIC_PLASTIC_KIN,Q_ELASTIC_PLASTIC_KIN             = 0,0
        Plot_on=([False,False,False,False,False,False,False,False,False])
        title=(['','','','','','','','','','',''])
        
        # ELASTIC HOOK PLOTSETTINGS
        if self.CB_COMBI_HOOK.isChecked()==True: 
            title[1]='ELASTIC HOOK' 
            Plot_on[1]=True
            number_of_plots=2
            models=models+1
        # NEO HOOK PLOTSETTINGS   
        if self.CB_COMBI_NEO_HOOK.isChecked()==True: 
            title[2]='NEO HOOK' 
            Plot_on[2]=True
            number_of_plots=3
            models=models+1
        # MAXWELL PLOTSETTINGS   
        if self.CB_COMBI_MAXWELL.isChecked()==True: 
            title[3]='MAXWELL' 
            Plot_on[3]=True
            number_of_plots=4
            models=models+1
        # KELVIN VOIGT PLOTSETTINGS   
        if self.CB_COMBI_KELVIN_VOIGT.isChecked()==True: 
            title[4]='KELVIN VOIGT' 
            Plot_on[4]=True
            number_of_plots=5
            models=models+1 
        # ZENER PLOTSETTINGS   
        if self.CB_COMBI_ZENER.isChecked()==True: 
            title[5]='ZENER' 
            Plot_on[5]=True
            number_of_plots=6
            models=models+1    
        # PERZYNA PLOTSETTINGS   
        if self.CB_COMBI_PERZYNA.isChecked()==True: 
            title[6]='PERZYNA' 
            Plot_on[6]=True
            number_of_plots=7
            models=models+1
        # ELASTIC PLASTIC ISO PLOTSETTINGS   
        if self.CB_COMBI_ELASTIC_PLASTIC_ISO.isChecked()==True: 
            title[7]='ELASTIC PLASTIK ISO HARDENING' 
            Plot_on[7]=True
            number_of_plots=8
            models=models+1    
        # ELASTIC PLASTIC KIN PLOTSETTINGS   
        if self.CB_COMBI_ELASTIC_PLASTIC_KIN.isChecked()==True: 
            title[8]='ELASTIC PLASTIK KIN HARDENING' 
            Plot_on[8]=True
            number_of_plots=9
            models=models+1      
        # =====================================================================
        #      MODEL Computing
        # =====================================================================
        
        for i in range(1,self.NCYCLES):
            dEPS   = np.interp(T,self.fdEPST[1,:],self.fdEPST[0,:])
            # =================================================================
            #           HOOK
            # =================================================================
            if self.CB_COMBI_HOOK.isChecked()==True:
                SIG_HOOK=model.hook(SIG_HOOK,dEPS,
                                    self.VAL_E_HOOK.value(),
                                    self.VAL_DT.value())
            self.DATA[i,2]=SIG_HOOK    
            # =================================================================
            #           NEO HOOK      
            # =================================================================
            if self.CB_COMBI_NEO_HOOK.isChecked()==True:
                SIG_NEO_HOOK=model.hook(SIG_NEO_HOOK,dEPS,
                                        self.VAL_E_NEO_HOOK.value(),
                                        self.VAL_DT.value())
            self.DATA[i,3]=SIG_NEO_HOOK    
            # =================================================================
            #          MAXWELL       
            # =================================================================
            if self.CB_COMBI_MAXWELL.isChecked()==True:
                SIG_MAXWELL=model.maxwell(SIG_MAXWELL, dEPS,
                                               self.VAL_E_MAXWELL.value(),
                                               self.VAL_ETA_MAXWELL.value(),
                                               self.VAL_DT.value()) 
            self.DATA[i,4]=SIG_MAXWELL                                           
            # =================================================================
            #          KELVIN VOIGT       
            # =================================================================
            if self.CB_COMBI_KELVIN_VOIGT.isChecked()==True:
                SIG_KELVIN_VOIGT=model.kelvinvoigt(EPS, dEPS,
                                                   self.VAL_E_KELVIN_VOIGT.value(),
                                                   self.VAL_ETA_KELVIN_VOIGT.value(),
                                                   self.VAL_DT.value())
            self.DATA[i,5]=SIG_KELVIN_VOIGT    
            # =================================================================
            #          ZENER       
            # =================================================================
            if self.CB_COMBI_ZENER.isChecked()==True:
                SIG_ZENER,EPS_D_ZENER=model.zener(SIG_ZENER,dEPS,EPS_D_ZENER,
                                                  EPS,self.VAL_E1_ZENER.value(),
                                                  self.VAL_E2_ZENER.value(),
                                                  self.VAL_ETA_ZENER.value(),
                                                  self.VAL_DT.value())
            self.DATA[i,6]=SIG_ZENER    
            # =================================================================
            #          PERZYNA    
            # =================================================================
            if self.CB_COMBI_PERZYNA.isChecked()==True:
                SIG_PERZYNA=model.perzyna(SIG_PERZYNA,dEPS,
                                          self.VAL_E_PERZYNA.value(),
                                          self.VAL_ETA_PERZYNA.value(),
                                          self.VAL_SIGMA_Y_PERZYNA.value(),
                                          self.VAL_DT.value())
            self.DATA[i,7]=SIG_PERZYNA
            # =================================================================
            #          ELASTIC PLASTIC IOS    
            # =================================================================
            if self.CB_COMBI_ELASTIC_PLASTIC_ISO.isChecked()==True:
                SIG_ELASTIC_PLASTIC_ISO,ALPHA_ELASTIC_PLASTIC_ISO=model.elsatic_plastic_iso( 
                    SIG_ELASTIC_PLASTIC_ISO,
                    dEPS,
                    self.VAL_E_ELASTIC_PLASTIC_ISO.value(),
                    self.VAL_SIGMA_Y_ELASTIC_PLASTIC_ISO.value(),
                    self.VAL_DT.value(),
                    self.VAL_K_ELASTIC_PLASTIC_ISO.value(),
                    ALPHA_ELASTIC_PLASTIC_ISO)
                                        
            self.DATA[i,8]= SIG_ELASTIC_PLASTIC_ISO
            
            # =================================================================
            #          ELASTIC PLASTIC IOS    
            # =================================================================
            if self.CB_COMBI_ELASTIC_PLASTIC_KIN.isChecked()==True:
                SIG_ELASTIC_PLASTIC_KIN,Q_ELASTIC_PLASTIC_KIN=model.elsatic_plastic_kin( 
                    SIG_ELASTIC_PLASTIC_KIN,
                    dEPS,
                    self.VAL_E_ELASTIC_PLASTIC_KIN.value(),
                    self.VAL_SIGMA_Y_ELASTIC_PLASTIC_KIN.value(),
                    self.VAL_DT.value(),
                    Q_ELASTIC_PLASTIC_KIN,
                    self.VAL_H_ELASTIC_PLASTIC_KIN.value())
                                        
            self.DATA[i,9]= SIG_ELASTIC_PLASTIC_KIN
            # =================================================================
            #          TIME AND EPSILON       
            # =================================================================
            EPS = EPS + dEPS *  self.VAL_DT.value()
            T=T+ self.VAL_DT.value()
            self.DATA[i,0]=T
            self.DATA[i,13]=EPS
            
        # =====================================================================
        #   COMBINE MODELS          
        # =====================================================================
        if models>1 and  self.CB_COMBI.isChecked()==True:
            title[0]='COMBIMODEL' 
            Plot_on[0]=True
            for i in range(0,number_of_plots):
                 print(i)
                 self.DATA[:,1]=self.DATA[:,1]+self.DATA[:,i+1]
        # =====================================================================
        #   PLOT ONLY COMBINE MODEL         
        # =====================================================================         
        if self.CB_COMBI_SPLIT.isChecked()==False and models>1:
            number_of_plots=1
        # =====================================================================
        #   PLOT STRESS OVER TIME        
        # =====================================================================
        self.plot_in_gui(self.DATA[:,0],self.DATA,title,
                             'Time [sec]','$\sigma$ [MPa]',
                             'STRESS OVER TIME','STRESS_TIME',Plot_on,
                             number_of_plots=number_of_plots)
        # =====================================================================
        #   PLOT STRESS OVER STRAIN        
        # =====================================================================
        self.plot_in_gui(self.DATA[:,13],self.DATA,title,
                             '$\epsilon$ [mm]','$\sigma$ [MPa]',
                             'STRESS OVER STRAIN','STRESS_STRAIN',Plot_on,
                             number_of_plots=number_of_plots)


# =============================================================================
# START APP
# =============================================================================
  
app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.set_loading()
window.plot_model()
window.show()
app.exec_()





