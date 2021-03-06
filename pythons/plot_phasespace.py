#!/usr/bin/python
######################################################################
# Name:         ALaDyn_plot_phasespace.py
# Author:       A. Marocchino, F. Mira, N. Panzeri
# Date:         2016-11-03
# Purpose:      reads ALaDyn binary from PDBunch* and plots phasespace
# Source:       python
#####################################################################
import os, sys, struct
from scipy import *
import numpy as np
import pylab as pyl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
###>>>
sys.path.append(os.path.join(os.path.expanduser('~'),'Codes/ALaDyn_Code/tools-ALaDyn/pythons'))
###>>>
### --- ###
from read_particle_phasespace import *
from utilities_1 import *
### --- ###


# --- # --- # --- #
### --- ### shell inputs
if(len(sys.argv)<9):
	print 'Usage :: python ~/Codes/tools-ALaDyn/ALaDyn_Pythons/plot_phasespace.py 0 9 -1 -1 0 1000 10 1 5'
	print 'Not enough arguments >>>'
	print ''
	print 'frame begin'
	print 'frame end'
	print 'selection via Weights: all particles with weight less then INput :: -1 for all particles'
	print 'gamma cut: only particle with gamma greater then INput :: -1 for all particles'
	print 'longitudinal min cut: remove particle with X less than INput :: -1 for no cut'
	print 'longitudinal max cut: remove particle with X greater than INput  :: -1 for no cut'
	print 'transverse cut: remove particle with R greater than INput  :: -1 for no cut'
	print 'particle Jump: one every jump particle'
	print 'slice analysis: slice longitudinal dimension in um'
	print ''
	exit('---not enough arguments---')
#---
frame_begin = int(sys.argv[1])
frame_end   = int(sys.argv[2])
W_threshold = float(sys.argv[3])
gamma_threshold   = float(sys.argv[4])
Xmin_threshold = float(sys.argv[5])
Xmax_threshold = float(sys.argv[6])
transverse_threshold = float(sys.argv[7])
jump = int(sys.argv[8])
slice_um  = float(sys.argv[9])

#-path
path = os.getcwd()
#-folder output structure
generate_folder_phasespace(path)

#--- ***  mining and printing ***---#
for i in range(frame_begin, frame_end + 1 ):
	print '-------------------'
	s='%2.2i'%i
	path_read  = os.path.join(path,'%4.4i'%i)
	path_write = path
	if output_exists(path_read,'phasespace',i) == True:
		print 'Analysing Phase Space --- frame >>> ',i

		X = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','X')
		number_of_particles = len(X); del X
		p_selected = np.full((number_of_particles), True, dtype=bool)
		# gamma_selected = np.full((number_of_particles), True, dtype=bool)
		# W_selected = np.full((number_of_particles), True, dtype=bool)
		# X_selected = np.full((number_of_particles), True, dtype=bool)
		# R_selected = np.full((number_of_particles), True, dtype=bool)

		#--- jump ---#
		p_selected[0:jump:number_of_particles]=False

		if(gamma_threshold>-1.):
			Px = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Px')
			gamma = 1.+Px**2
			del Px
			Py = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Py')
			gamma = gamma+Py**2
			del Py
			Pz = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Pz')
			gamma = gamma+Pz**2
			del Pz
			gamma=np.array(np.sqrt(gamma))
			p_selected = (gamma>gamma_threshold)
			del gamma

		if(W_threshold>-1.):
			W = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','W')
			p_selected = (p_selected & (W<=W_threshold) )

		if(Xmin_threshold> -1):
			X = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','X')
			p_selected = (p_selected & (X>=Xmin_threshold) )
			del X
		if(Xmax_threshold> -1):
			X = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','X')
			p_selected = (p_selected & (X<=Xmax_threshold) )
			del X

		if(transverse_threshold > -1):
			Y = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Y')
			p_selected = (p_selected & (abs(Y)<=transverse_threshold) )
			del Y
			Z = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Z')
			p_selected = (p_selected & (abs(Z)<=transverse_threshold) )
			del Z

		# --- *** --- #
		Px = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Px')
		Px = Px[p_selected]
		Py = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Py')
		Py = Py[p_selected]
		Pz = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Pz')
		Pz = Pz[p_selected]
		X = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','X')
		X = X[p_selected]
		Y = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Y')
		Y = Y[p_selected]
		Z = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','Z')
		Z = Z[p_selected]
		W = read_particle_phasespace_bycomponent( path_read,'Elpout'+s+'.bin','W')
		W = W[p_selected]

		#--- *** diagnostics *** ---#
		Charge  =  read_electrons_ppm( path_read,'Elpout'+s+'.dat')*np.sum(W)*1.6e-7
		sigmax  = np.std(X)
		sigmay  = np.std(Y)
		Current = Charge*1e-15*3e8/np.sqrt(2*np.pi)/sigmax/1e-6
		gamma = np.array(np.sqrt(1. + Px**2 + Py**2 + Pz**2))
		en_spread = round(np.std(gamma)/np.mean(gamma)*100,1)
		emittance_y = np.sqrt( np.std(Y)**2*np.std(Py)**2-np.cov(Y,Py)[0][1]**2);
		emittance_z = np.sqrt( np.std(Z)**2*np.std(Pz)**2-np.cov(X,Pz)[0][1]**2);

		print 'Diagnostic for the whole bunch'
		print 'Energy spread: ', ('%3.2e' % en_spread) ,'%'
		print 'Normalized Emittance Y: ', (round(emittance_y,2)), 'mm-mrad'
		print 'Normalized Emittance Z: ', (round(emittance_z,2)), 'mm-mrad'
		print 'Mean Energy: ', round(np.mean(gamma)*0.51,1), 'MeV'
		print 'Charge:',('%3.2e' % Charge), 'pC'
		print 'Peak Current:',('%3.2e' % Current), 'kA'
		print 'Sigmax:',('%3.2e' % sigmax),'mum'
		print 'Sigmay:',('%3.2e' % sigmay),'mum'
		plt.figure(figsize=(20,10))
		#fig=plt.figure()
		#ax=fig.add_subplot(111,projection='3d')
		#ax.scatter(X,Y,Z,s=.05,edgecolors='None')
		#ax.set_xlabel('X')
		#ax.set_xlabel('Y')
		#ax.set_xlabel('Z')
		plt.subplot(311)
		plt.scatter(X,Px,s=.1,edgecolors='None')
		#plt.scatter(X,Y,Z,s=.1,edgecolors='None')
		#plt.xlabel(r'$X (\mu m) $');plt.ylabel(r'$Z (\mu m)$')
		plt.xlabel(r'$X (\mu m) $',fontsize=24,fontweight='bold');plt.ylabel(r'$P_x/mc$',fontsize=24,fontweight='bold')
		#plt.text(90,327, r'$Energy spread = 20,2% $',size=18,ha='left',va='top')
		plt.subplot(312)
		#       plt.scatter(Y,Z,s=.1,edgecolors='None')
		#       plt.xlabel(r'$Y (\mu m) $');plt.ylabel(r'$Z (\mu m)$')
#		plt.scatter(Y,Py,s=.1,edgecolors='None')
#		plt.xlabel(r'$Y (\mu m)$',fontsize=24,fontweight='bold');plt.ylabel(r'$P_y/mc$',fontsize=24,fontweight='bold')
                plt.scatter(Y,Py,s=.1,edgecolors='None')
                plt.xlabel(r'$Y (\mu m)$',fontsize=24,fontweight='bold');plt.ylabel(r'$P_y/mc$',fontsize=24,fontweight='bold')
		plt.subplot(313)
		#       plt.scatter(X,Y,s=.1,edgecolors='None')
		#      plt.xlabel(r'$X (\mu m) $');plt.ylabel(r'$Y (\mu m)$')
		#plt.scatter(Pz,Py,s=.1,edgecolors='None')
		#plt.xlabel('Pz/mc');plt.ylabel('Py/mc')
		#plt.subplot(313)
		plt.hist(gamma*0.511,300)
		#       plt.hist(gamma[gamma_selected],50)
		plt.xlabel('$Energy (MeV)$',fontsize=24,fontweight='bold');plt.ylabel('$dN/dE$',fontsize=24,fontweight='bold');
		#       plt.axis('tight')
		plt.subplots_adjust(left=0.08,right=0.8,hspace=0.45)
		name_output = 'Phsp_enspect'+'_'+('%2.2i'%i)+'.png'
		#np.savetxt('X_'+('%2.2i'%i)+'.txt',X)
                #np.savetxt('Px_'+('%2.2i'%i)+'.txt',Px)
		#name_output =  '3Dplot' + '_' +('%2.2i'%i)+ '.png'
		plt.savefig( os.path.join(path_write,'data','phasespace',name_output) )
		#plt.close()
		plt.show()



		#--- *** Slice diagnostics ***---#
		first_particle_x=np.min(X)
		last_particle_x=np.max(X)
		slice_x_min=first_particle_x
		slice_x_max=slice_x_min+slice_um
		slice_counter=0
		print 'slice_counter,Charge, sigma_x,sigma_y,gamma-mean,energy_spread, emittance_y, emittance_z'
		while (last_particle_x>slice_x_max):
			X_selected = (X>slice_x_min & X<slice_x_max)

			Charge  =  read_electrons_ppm(path_read,'Elpout'+s+'.dat')*np.sum(W[X_selected])*1.6e-7
			sigmax  = np.std(X[X_selected])
			sigmay  = np.std(Y[X_selected])
			Current = Charge*1e-15*3e8/np.sqrt(2*np.pi)/slice_um/1e-6
			gamma = np.array(np.sqrt(1. + Px**2 + Py**2 + Pz**2))
			en_spread = round(np.std(gamma[X_selected])/np.mean(gamma[X_selected])*100,1)
			emittance_y = np.sqrt( np.std(Y[X_selected])**2*np.std(Py[X_selected])**2-np.cov(Y[X_selected],Py[X_selected])[0][1]**2);
			emittance_z = np.sqrt( np.std(Z[X_selected])**2*np.std(Pz[X_selected])**2-np.cov(X[X_selected],Pz[X_selected])[0][1]**2);

			print slice_counter,Charge,sigmax,sigmay,np.mean(gamma[X_selected]),en_spread,emittance_y,emittance_z

			slice_x_min+=slice_um
			slice_x_max+=slice_um
			slice_counter+=1

	else:
		print '--- --- ---'
