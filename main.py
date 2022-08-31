from time import sleep
from faculty import Faculty, inc_flag
from input import load
from random import shuffle
import sqlite3
import datetime

fac_dict = {}
HoD = [Faculty("Dr. H V Ravish Aradhya", 0, "HoD", 1, 1, "HoD")]					# Get HoD
room_list = [chr(i+65) for i in range(10)]

def get_faculty(designation, index, load_all = 0):
	fac_list = []
	global fac_dict
	fac_list=list(filter(lambda fac:fac.designation==designation, fac_dict[index]))
	return fac_list

def random_unique(rep, added_list, designation, experience=0):
	unique_list = []
	i = 0
	while(len(unique_list)<rep):
		fac_list = get_faculty(designation, i)
		fac_list2=[]

		for fac in fac_list:
			flag=0
			for fac2 in added_list:
				if fac==fac2:
					flag=1
			if flag==0:
				fac_list2.append(fac)
		fac_list = fac_list2
		if experience:
			fac_list = list(filter(lambda fac:fac.experience==1, fac_list))
		if i>=1000:
			raise Exception("Enough staff not available")
		shuffle(fac_list)
		unique_list += fac_list
		i+=1
	return unique_list[0:rep]

class Allocate:
	def __init__(self):
		global fac_dict
		fac_dict = {}
		fac_dict[0] = load()			# load return a list of faculties
		for i in range(1, 1000):
			fac_dict[i] = []
		self.sessions = [[] for i in range(1+6)] # Staff same for all 6 sessions plus session wise staff allocation
		self.filename = str(datetime.datetime.now())+".db"

	def allocate(self, n):
		comman = self.sessions[0][0]+self.sessions[0][2]
		DySp = random_unique(1,self.sessions[n-1][0], "Professor")
		for fac in DySp:
			fac.flag+=1
			fac_dict[fac.flag-1].remove(fac)
			fac_dict[fac.flag].append(fac)
			fac.role = "DySp"
		print(f'\nDEPUTY SUPERINTENDENT = {DySp}\n')

		invigilators = random_unique(10, self.sessions[n-1][1]+comman, "Assistant Professor")
		for fac in invigilators:
			fac.flag+=1
			fac_dict[fac.flag-1].remove(fac)
			fac_dict[fac.flag].append(fac)
			fac.role = "Invigilator"
		print(f'INVIGILATORS = {invigilators}\n')

		reliever = random_unique(3, self.sessions[n-1][2], "Associate Professor")
		for fac in reliever:
			fac.flag+=1
			fac_dict[fac.flag-1].remove(fac)
			fac_dict[fac.flag].append(fac)
			fac.role = "Reliever"
		print(f'RELIEVER = {reliever}\n')

		self.sessions[n] = [DySp]+[invigilators]+[reliever]
		roles = ["DySp", "Invigilator", "Reliever"]

		con = sqlite3.connect(self.filename)
		cur = con.cursor()
		create_query = f"CREATE TABLE {'session'+str(n)} ( \n name text,\n role text,\n room no text)"
		cur.execute(create_query)
		for fac_list in self.sessions[n]:
			for fac in fac_list:
				result = cur.execute( f"Insert into {'session'+str(n)} values(?, ?, ?)" ,get_query(fac_list, fac, n))
		con.commit()
		con.close()

	def allocate_comman(self):
		backup = random_unique(3, [], "Assistant Professor")
		for fac in backup:
			fac.role = "Backup"
		print(f'BACKUP = {backup}\n')

		squad = random_unique(4, backup, "Assistant Professor", experience = 1)
		for fac in squad:
			fac.flag+=3
			fac_dict[fac.flag-3].remove(fac)
			fac_dict[fac.flag].append(fac)
			fac.role = "Squad"
		print(f'SQUAD = {squad}\n')

		global HoD
		for fac in HoD:
			fac.flag+=1		#What to put?
			fac.role = "HoD"
		print(f'HoD = {HoD}')
		self.sessions[0]=[squad]+[HoD]+[backup]+[[]]+[[]]+[[]]	#Empty list added so that allocate does not throw error for first session	
		roles = ["Backup", "Squad", "HoD"]
		con = sqlite3.connect(self.filename)
		cur = con.cursor()
		create_query = f"CREATE TABLE comman ( \n name text,\nrole text,\nroom_no text)"
		#print(create_query)
		cur.execute(create_query)
		for fac_list in self.sessions[0]:
			for fac in fac_list:
				result = cur.execute( f"Insert into comman values(?, ?, ?)",get_query(fac_list, fac) )
		con.commit()
		con.close()

def get_query(fac_list, fac, n=0):
	global room_list
	l = [fac.name, fac.role]
	if fac.role=="Invigilator":
		for i in range(len(room_list)):
			if fac_list.index(fac)==i:
				room = room_list[i]
		l.append(room)
	elif fac.role=="Reliever":
		rooms = []
		a = list(split(range(len(room_list)), 3))[fac_list.index(fac)]
		for i in range(len(room_list)):
			if i in a:
				rooms.append(room_list[i])
		l.append(", ".join(rooms))
	elif fac.role=="DySp":
		l.append("")
	elif fac.role=="Squad":
		l.append("")
	elif fac.role=="Backup":
		l.append("")
	elif fac.role=="HoD":
		l.append("")
	else:
		raise Exception(f"Role {fac.role} not correct")
	return tuple(l)

def split(a, n):
	k, m = divmod(len(a), n)
	return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def main():
	sessions = Allocate()
	sessions.allocate_comman()
	print("\n*****************Session 1***********************\n")
	sessions.allocate(1)
	print("\n*****************Session 2***********************\n")
	sessions.allocate(2)
	print("\n*****************Session 3***********************\n")
	sessions.allocate(3)
	print("\n*****************Session 4***********************\n")
	sessions.allocate(4)
	print("\n*****************Session 5***********************\n")
	sessions.allocate(5)
	print("\n*****************Session 6***********************\n")
	sessions.allocate(6)
	return sessions


if __name__ == '__main__':
	sessions = main()

##############
""" Sessions = List of session
	Session = List of combination of DySp, Squad, Invigilator, Backup, Reliever
	Invigilator = List of faculty objects
"""

"""Model 1
400 students 10 classroom
Rvce ECE staff structure
HOD-1 (CS)
Prof-5(DSP)
Associate prof- 10(rel/squad)
Assist prof-35(squa/rs)

Inputs-
•	 Excel sheets
•	 Gender
•	 Designation names
•	 Experience(Hi/Lo)
Number of days number of shifts
Previous exam history.
Computation:
Creating variables
Level 1:
Random selection:
•	 1 out of 5 - prof
•	 Squad 4 (2 +2) out of 35 ast p
•	 10 out of 31-astp
•	 3 out of 10-aso P
•	 HOD
•	 Backup 3out of 21 astp
Level 2					  //Afternoon Session
Module sel
No rep selection:
•	 10 out of 21-astp
•	 3 out of 7-aso P
•	 1out of 4- prof
•	 3 out of 11
Level 3
10 out of 21
3 out of7
1 out of 4
3 out 11

Flag
•	 Random selection of AP, P, ASSpof
•	 If duty then duty=duty+1

Range 1-5 Professors
6-14 Associate
15-48 Assistant
"""

