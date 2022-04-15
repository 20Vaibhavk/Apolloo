import mysql.connector as mycon
mydb = mycon.connect(host="localhost", user="root", password="", database="apollodb")
mycur = mydb.cursor()

return mycur