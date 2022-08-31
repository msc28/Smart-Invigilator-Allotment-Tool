from random import choice

def reallocate_prior(fac, backup_list, fac_list):
	fac = choice(backup_list)
	fac.dec_flag()
	new_fac.inc_flag()
	return new_fac

def reallocate_emergency(fac, role, fac_dict): #fac_list should be after that round of allocation
	#First decide if we will take fac_dict for the sessions list
	return new_fac

if __name__=='__main__':
	fac = #Name or id of faculty
	role = #Query from db
	fac_dict = #fac_dict from main
	backup_list = #get available backup
	new_fac = reallocate_prior(fac, backup_list)
	if new_fac == -1:
		new_fac = reallocate_emergency(fac, role, fac_dict)
	#update in db
