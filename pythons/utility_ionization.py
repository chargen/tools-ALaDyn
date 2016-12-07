#!/usr/bin/python
######################################################################
# Name:         ALaDyn_plot_utilities_Efield.py
# Author:       A. Marocchino
# Date:			2014-02-18
# Purpose:      it is a module of: ALaDyn_plot_sections - plots densities
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, time, datetime
import numpy as np
from pylab import *
from matplotlib import colors, ticker, cm
###>>>
# home_path = os.path.expanduser('~')
# sys.path.append(os.path.join(home_path,'Codes/ALaDyn_Code/tools-ALaDyn/ALaDyn_Pythons'))
###>>>
from read_ALaDyn_bin import *
from utilities_1 import *
### --- ###






#- plot Sections
def plot_ionization_profile(path,frame,min_ionization_rate,max_ionzation_rate,isolines,celltocut,sliceposition_x,sliceposition_y,sliceposition_z,magnification_fig,savedata):
	s='%2.2i'%frame 				#conversion to 2-character-long-string


# 	file_name = 'Elpout'+s+'.bin'
	file_name = 'H1dnout'+s+'.bin'
	matrix,  x,y,z = read_ALaDyn_bin(path,file_name,'grid')	
	
	#- cut & sign
	matrix = np.abs( matrix )

	#---cut edges---#
	if celltocut > 0:
		matrix  = matrix[:,celltocut:-celltocut,celltocut:-celltocut]
		y		= y[celltocut:-celltocut]
		z		= z[celltocut:-celltocut]

	p = matrix.shape
	x2=p[0]/2+sliceposition_x; y2=p[1]/2+sliceposition_y; z2=p[2]/2+sliceposition_z;
	
	sizeX, sizeZ = figure_dimension_inch(x,y,z,magnification_fig)

# 	levs_lin = np.linspace(      rho_min ,      rho_max ,isolines)
# 	levs_lin = np.insert(levs_lin,0,np.min([np.min(matrix),np.min(matrix2)]))
# 	levs_lin = np.insert(levs_lin,len(levs_lin),np.min([np.max(matrix),np.max(matrix2)]))
# 	levs_log = np.logspace(log10(rho_min),log10(rho_max),isolines)


	#--------------------#
	#--- Linear plots ---#
	#--------------------#
	#- Plot Bdenout -#
#	fig = figure(1, figsize=(sizeX, sizeZ))
#	contourf(x,y,matrix[:,:,z2].T,levs_lin, linewidths = 0.00001)
#	axis('tight')
#	name_output = 'rho_Bunch_XY_lin_'+s+'.png'
#	savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)
#
#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,z,matrix[:,y2,:].T,levs_lin, linewidths = 0.00001)
#	axis('tight')
#	name_output = 'rho_Bunch_XZ_lin_'+s+'.png'
#	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

# 	fig = figure(1, figsize=(sizeZ, sizeZ))	
# 	contourf(y,z,matrix[x2,:,:].T,levs_lin, linewidths = 0.00001)
#	axis('tight')
# 	name_output = 'rho_Bunch_YZ_lin_'+s+'.png'
# 	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)



	#- Plot Edenout -#
#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,y,matrix2[:,:,z2].T,levs_lin, linewidths = 0.00001)
#	axis('tight')
#	name_output = 'rho_Background_XY_lin_'+s+'.png'
#	savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,z,matrix2[:,y2,:].T,levs_lin, linewidths = 0.00001)
#	axis('tight')
#	name_output = 'rho_Background_XZ_lin_'+s+'.png'
#	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

# 	fig = figure(1, figsize=(sizeZ, sizeZ))	
# 	contourf(y,z,matrix2[x2,:,:].T,levs_lin, linewidths = 0.00001)
#	axis('tight')
# 	name_output = 'rho_Background_YZ_lin_'+s+'.png'
# 	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)



	#- Plot Bdenout+Edenout -#
#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,y,matrix[:,:,z2].T + matrix2[:,:,z2].T,levs_lin, linewidths = 0.00001)
#	axis('tight')
#	name_output = 'rho_tot_XY_lin_'+s+'.png'
#	savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,z,matrix[:,y2,:].T + matrix2[:,y2,:].T,levs_lin, linewidths = 0.00001)
#	axis('tight')
#	name_output = 'rho_tot_XZ_lin_'+s+'.png'
#	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

# 	fig = figure(1, figsize=(sizeX, sizeX))	
# 	contourf(y,z,matrix[x2,:,:].T - matrix2[x2,:,:].T,levs_lin, linewidths = 0.00001)
#	axis('tight')
# 	name_output = 'rho_tot_YZ_lin_'+s+'.png'
# 	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)










	#--------------------#
	#---  Log plots   ---#
	#--------------------#
	#- Plot Bdenout -#
#	fig = figure(1, figsize=(sizeX, sizeZ))
#	contourf(x,y,matrix[:,:,z2].T, levs_log, norm=colors.LogNorm())
#	axis('tight')
#	name_output = 'rho_Bunch_XY_log_'+s+'.png'
#	savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,z,matrix[:,y2,:].T,levs_log, norm=colors.LogNorm())
#	axis('tight')
#	name_output = 'rho_Bunch_XZ_log_'+s+'.png'
#	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

# 	fig = figure(1, figsize=(sizeZ, sizeZ))	
# 	contourf(y,z,matrix[x2,:,:].T, levs_log, norm=colors.LogNorm())
#	axis('tight')
# 	name_output = 'rho_Bunch_YZ_log_'+s+'.png'
# 	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)



	#- Plot Edenout -#
#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,y,matrix2[:,:,z2].T, levs_log, norm=colors.LogNorm())
#	axis('tight')
#	name_output = 'rho_Background_XY_log_'+s+'.png'
#	savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,z,matrix2[:,y2,:].T, levs_log, norm=colors.LogNorm())
#	axis('tight')
#	name_output = 'rho_Background_XZ_log_'+s+'.png'
#	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

# 	fig = figure(1, figsize=(sizeZ, sizeZ))	
# 	contourf(y,z,matrix2[x2,:,:].T, levs_log, norm=colors.LogNorm())
#	axis('tight')
# 	name_output = 'rho_Background_YZ_log_'+s+'.png'
# 	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)



	#- Plot Bdenout+Edenout -#
#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,y,matrix[:,:,z2].T + matrix2[:,:,z2].T,levs_log , norm=colors.LogNorm())
#	axis('tight')
#	name_output = 'rho_tot_XY_log_'+s+'.png'
#	savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

#	fig = figure(1, figsize=(sizeX, sizeZ))	
#	contourf(x,z,matrix[:,y2,:].T + matrix2[:,y2,:].T,levs_log , norm=colors.LogNorm())
#	axis('tight')
#	name_output = 'rho_tot_XZ_log_'+s+'.png'
#	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)

# 	fig = figure(1, figsize=(sizeX, sizeX))	
# 	contourf(y,z,matrix[x2,:,:].T + matrix2[x2,:,:].T, levs_log, norm=colors.LogNorm())
#	axis('tight')
# 	name_output = 'rho_tot_YZ_log_'+s+'.png'
# 	fig.savefig( os.path.join(path,'plots','rho',name_output) )
#	close(fig)



    #----- Save density sections data -----#
	if (savedata == 'True'):
    	
		print 'saving ionization data'
    	
		ionization_map = matrix
		

		ionization_map=np.abs( ionization_map )
		
		p = ionization_map.shape
		x2=p[0]/2+sliceposition_x; y2=p[1]/2+sliceposition_y; z2=p[2]/2+sliceposition_z;		
		
	
		np.savetxt( os.path.join(path,'data','ionization',('ionization_profile_'+('%2.2i'%frame)+'.dat')),ionization_map[:,:,z2].T,fmt='%15.14e')

# 		np.savetxt( 'rho_section_'+('%2.2i'%frame)+'.dat' ,rho[:,:,z2].T,fmt='%15.14e')
# 		np.savetxt( 'rho_b_section_'+('%2.2i'%frame)+'.dat' ,rho_b[:,:,z2].T,fmt='%15.14e')


