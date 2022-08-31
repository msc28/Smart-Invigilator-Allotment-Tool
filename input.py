#Structure of Excel File
#Index | Name | Email-id | Designation

from faculty import Faculty
from sys import argv
import sqlite3

def load():
    con = sqlite3.connect('inputdb.sqlite')
    cur = con.cursor()
    f_list = []
    p_list = []
    asop_list = []
    assp_list = []
    others = []
    cur.execute('''SELECT count(*) FROM ece''')
    n = int(cur.fetchone()[0])

    for i in range(1, n+1): #i -> row
        cur.execute('''SELECT * FROM ece WHERE ROWID=?''',(i,))

        r=cur.fetchone()

        #if(sheet1.cell(row=i, column=1).value != None):

            #print(str(sheet1.cell(row=i, column=2).value))

        if(r[2] =='Professor'):

            p_list.append(Faculty(r[0], r[5], r[2], r[3], r[4], ""))

        elif(r[2]=='Associate Professor'):

            asop_list.append(Faculty(r[0], r[5], r[2], r[3], r[4], ""))

        elif(r[2]=='Assistant Professor'):

            assp_list.append(Faculty(r[0], r[5], r[2], r[3], r[4], ""))

        else:
            others.append(Faculty(r[0], r[5], r[2], r[3], r[4], ""))
    f_list = p_list+asop_list+assp_list
    assert(len(others)==0)
    return f_list

if __name__ == '__main__':
    f_list = load()
    print(*f_list, sep="\n")		# * is print the list without brackets ( '[', ']' )
