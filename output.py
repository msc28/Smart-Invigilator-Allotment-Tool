from openpyxl import load_workbook, Workbook
from main import main
from input import load

debug = False

fac_list = load()			
sessions = main()
wb = Workbook()
dest_filename = 'output.xlsx'
ws1 = wb.active
ws1.title = "Allocation Chart"
for i in range(1, 7):			#Session no.
	hrow = str(12*(i-1)+1)		#Header row
	hrow_i = int(hrow)
	ws1['A'+hrow] = "Session "+str(i)
	ws1['B'+hrow] = "Room no."

	for j in range(hrow_i+1, hrow_i+11):
		ws1['B'+str(j)] = str(j-hrow_i)
	if debug:
		print("Done room no.")
	ws1['C'+hrow] = "Invigilators"
	for j in range(hrow_i+1, hrow_i+11):
		try:
			ws1['C'+str(j)] = sessions[i-1][2][j-hrow_i-1].name
		except:
			ws1['C'+str(j)] = ""
	if debug:
		print("Done Invigilators")
	ws1['D'+hrow] = ""
	ws1['E'+hrow] = "Squad"
	for j in range(hrow_i+1, hrow_i+11):
		try:
			ws1['E'+str(j)] = sessions[i-1][1][j-hrow_i-1].name
		except:
			ws1['E'+str(j)] = ""
	if debug:
		print("Done Squad")
	ws1['F'+hrow] = "Dy Sp"
	for j in range(hrow_i+1, hrow_i+11):
		try:
			ws1['F'+str(j)] = sessions[i-1][0][j-hrow_i-1].name
		except:
			ws1['F'+str(j)] = ""
	if debug:
		print("Done DySp")	
	ws1['G'+hrow] = "Sp"
	ws1['G'+str(hrow_i+1)] = "Dr. Geetha K.S."
	ws1['H'+hrow] = "Backup Invigilators"
	for j in range(hrow_i+1, hrow_i+11):
		try:
			ws1['H'+str(j)] = sessions[i-1][3][j-hrow_i-1].name
		except:
			ws1['H'+str(j)] = ""
	if debug:
		print("Done Backup")
	ws1['I'+hrow] = "Reliever"
	for j in range(hrow_i+1, hrow_i+11):
		try:
			ws1['I'+str(j)] = sessions[i-1][4][j-hrow_i-1].name
		except:
			ws1['I'+str(j)] = "" 
	if debug:
		print("Done relievers")
			
wb.save(filename = dest_filename)

if debug:
	print("Done")