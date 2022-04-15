# Database setup and import required modules
import mysql.connector as mycon
mydb = mycon.connect(host="localhost", user="root", password="", database="apollodb")
mycur = mydb.cursor()

auth = [] # To save users credentials such as user ID

# Value returning/middleman functions
def getAuth(email, password, authType):
	if(authType == 'buyer'):
		sql = ("SELECT userId from users WHERE email=%s AND password=%s")
		val = (email, password)
		mycur.execute(sql, val)

		res = mycur.fetchall()

		if(res == []):
			print("User does not exists.")
		else:
			auth.append(res[0][0]) # Selecting User ID
			buyer()
	elif(authType == 'seller'):
		sql = ("SELECT sellerId from sellers WHERE email=%s AND password=%s")
		val = (email, password)
		mycur.execute(sql, val)

		res = mycur.fetchall()

		if(res == []):
			print("User does not exists.")
		else:
			auth.append(res[0][0]) # Selecting User ID
			seller()

def userExists(email, password, loginType):
	if(loginType == 'buyer'):
		sql = ("SELECT * FROM users WHERE email=%s AND password=%s")
		val = (email, password)
		mycur.execute(sql, val)

		res = mycur.fetchall()

		if(res != []):
			return True
		else:
			return False
	elif(loginType == 'seller'):
		sql = ("SELECT * FROM sellers WHERE email=%s AND password=%s")
		val = (email, password)
		mycur.execute(sql, val)

		res = mycur.fetchall()

		if(res != []):
			return True
		else:
			return False

# User authentication functions
def login():
	print("\n+-----------------------------------------------------------------+")
	email = input("Enter your email ")
	password = input("Enter your password ")
	loginType = input("Login as Buyer/Seller? ").lower()
	print("+-----------------------------------------------------------------+\n")
	UserExists = userExists(email, password, loginType)

	if(UserExists == True):
		getAuth(email, password, loginType)
	else:
		print("Your entered email or password is incorrect.")
		login()

def signup():
	print("\n+-----------------------------------------------------------------+")
	name = input("Enter your name ")
	email = input("Enter your email ")
	password = input("Enter your password ")
	signupType = input("Signup as Buyer/Seller ").lower()
	print("+-----------------------------------------------------------------+\n")

	if(signupType == 'buyer'):
		sql = ("INSERT into users(name, email, password) values(%s, %s, %s)")
		val = (name, email, password)
		mycur.execute(sql, val)
		mydb.commit()

		getAuth(email, password, signupType)
	elif(signupType == 'seller'):
		sql = ("INSERT into sellers(name, email, password) values(%s, %s, %s)")
		val = (name, email, password)
		mycur.execute(sql, val)
		mydb.commit()

		getAuth(email, password, signupType)

# Buyer dashboard and functions concerning buyer
def buyer():
	print("\n+================================================================+")
	print("1: Search a product 2: View Cart 0: Logout")
	print("+================================================================+\n")
	choice = int(input("Enter your choice "))

	if(choice == 1):
		searchProduct()
	elif(choice == 2):
		viewCart()
	elif(choice == 0):
		auth.clear()
		print("You are logged out.")
		main()

def viewCart():
	sql = ("SELECT cart.productId, products.productId, products.name, products.price, sellers.name FROM cart LEFT JOIN products ON products.productId=cart.product RIGHT JOIN sellers ON sellers.sellerId=cart.owner WHERE owner=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	count = 1
	print("\n+----------------------------------------------------------------+")
	for i in res:
		print(str(count) + ")",i[2],"-",i[3])
		count = count + 1
	print("+----------------------------------------------------------------+\n")

	print("1: Buyout the cart 2: Buy specific product 0: Go Back")
	choice = int(input("Select your choice "))

	if(choice == 1):
		for i in range(len(res)):
			buyProduct(res[i][1])
			sql = ("DELETE FROM cart WHERE productId=%s")
			val = (res[i][0],)
			mycur.execute(sql, val)
			mydb.commit()
		buyer()
	elif(choice == 2):
		selectProduct = int(input("Select product you want to buy "))
		sql = ("DELETE FROM cart WHERE productId=%s")
		val = (res[selectProduct - 1][0],)
		mycur.execute(sql, val)
		mydb.commit()
		buyProduct(res[selectProduct - 1][1])
		buyer()
	elif(choice == 0):
		buyer()

def searchProduct():
	productName = input("Enter product's name you want to buy ").lower()
	sql = ("SELECT products.productId, products.name, products.price, sellers.name, products.stock FROM products LEFT JOIN sellers ON products.seller=sellers.sellerId WHERE products.name=%s ORDER BY products.price ASC")
	val = (productName,)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res == []):
		print("Product does not exist on marketplace.")
	else:
		count = 1
		print("\n+----------------------------------------------------------------+")
		for i in res:
			if(i[4] != 0):
				stock = str(i[4]) + " left"
			else:
				stock = 'Out of Stock'
			print(str(count) + ")", i[1],"-",i[2],":",i[3],stock)
			count += 1
			print("\n------------------------------------------------------------------")
		print("+----------------------------------------------------------------+\n")
		selectProduct = int(input("Select a product "))

		productDetails(res[selectProduct - 1][0]) # Selecting Product ID

def productDetails(productId):
	print(productId)
	sql = ("SELECT products.productId, products.name, products.description, products.price, sellers.name FROM products LEFT JOIN sellers ON products.seller=sellers.sellerId WHERE products.productId=%s")
	val = (productId,)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res == []):
		print("Something went wrong.")
	else:
		for i in res:
			print("\n+----------------------------------------------------------------+")
			print(i[1])
			print("By",i[4])
			print("------------------------------------------------------------------")
			print("Description:",i[2])
			print("------------------------------------------------------------------")
			print("Price:",i[3])
			print("+----------------------------------------------------------------+\n")

			print("1: See Reviews 2: Buy Product 3: Add to Cart 0: Go Back")
			choice = int(input("Enter your choice "))

		if(choice == 1):
			showReviews(res[0][0]) # Selecting Product ID
		elif(choice == 2):
			buyProduct(res[0][0]) # Selecting Product ID
			buyer()
		elif(choice == 3):
			addToCart(res[0][0]) # Selecting Product ID
		elif(choice == 0):
			buyer()

def showReviews(productId):
	sql = ("SELECT users.name, ratings.rating, reviews.review FROM reviews LEFT JOIN users ON reviews.reviewBy=users.userId RIGHT JOIN ratings ON reviews.reviewBy=ratings.ratingBy WHERE reviews.product=%s")
	val = (productId,)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	print("\n+----------------------------------------------------------------+")
	for i in res:
		print(i[0],"-",i[1],"star rating")
		print(i[2])
		print("------------------------------------------------------------------")
	print("+----------------------------------------------------------------+\n")

	print("1: Leave a review 0: Go Back")
	choice = int(input("Enter your choice "))

	if(choice == 1):
		review = input("Write something about the product ")
		rating = int(input("Enter your rating about the product(1-5) "))

		if(rating > 5):
			rating = 5
		elif(rating < 1):
			rating = 1

		sql = ("INSERT INTO reviews(review, product, reviewBy) values(%s, %s, %s)")
		val = (review, productId, auth[0])
		mycur.execute(sql, val)
		mydb.commit()

		sql = ("INSERT INTO ratings(rating, product, ratingBy) values(%s, %s, %s)")
		val = (rating, productId, auth[0])
		mycur.execute(sql, val)
		mydb.commit()

		showReviews(productId)
	elif(choice == 0):
		productDetails(productId)

def buyProduct(productId):
	sql = ("INSERT INTO sales(product, boughtBy) values(%s, %s)")
	val = (productId, auth[0])
	mycur.execute(sql, val)
	mydb.commit()

	sql = ("UPDATE products SET stock=stock-1 WHERE productId=%s")
	val = (productId,)
	mycur.execute(sql, val)
	mydb.commit()

def addToCart(productId):
	sql = ("INSERT INTO cart(product, owner) values(%s, %s)")
	val = (productId, auth[0])
	mycur.execute(sql, val)
	mydb.commit()

	buyer()

# Seller dashboard and functions concerning seller
def seller():
	print("\n+================================================================+")
	print("1: Add product to your store 2: Add more stock 3: Check sales 0: Logout")
	print("+================================================================+\n")
	choice = int(input("Enter your choice "))

	if(choice == 1):
		addProduct()
	elif(choice == 2):
		addStock()
	elif(choice == 3):
		checkSales()
	elif(choice == 0):
		auth.clear()
		print("You are logged out.")
		main()

# Funtion to add a product to seller's catalog
def addProduct():
	name = input("Enter name of product ")
	description = input("Enter description of product in 280 characters")
	price = float(input("Enter price of the product "))
	stock = int(input("Enter the amount of stock you want to add "))

	sql = ("INSERT INTO products(name, description, price, stock, seller) values(%s, %s, %s, %s, %s)")
	val = (name, description, price, stock, auth[0])
	mycur.execute(sql, val)
	mydb.commit()

	print("Product was successfully added to your catalog.")
	seller()

# To help seller make sure stock is available to the user
def addStock():
	sql = ("SELECT name, productId FROM products WHERE seller=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	count = 1
	for i in res:
		print(str(count) + ")",i[0])
		count = count + 1

	selectProduct = int(input("Select the product you want to add stock to "))
	amount = int(input("Enter amount you want to add "))

	sql = ("UPDATE products SET stock=stock+%s WHERE productId=%s AND seller=%s")
	val = (amount, res[selectProduct - 1][1], auth[0])
	mycur.execute(sql, val)
	mydb.commit()
	seller()

# Check sales seller had
def checkSales():
	sql = ("SELECT products.price FROM products LEFT JOIN sales ON sales.product=products.productId WHERE seller=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	sales = 0
	for i in res:
		sales = sales + i[0]

	print("Products sold amounts at",sales)
	seller()

# Main funtion which is to be executed at very beginning(Have put it in last just to make sure every functions stores inside memory so their no problem concernig that)
def main():
	print("\n+-----------------------------------------------------------------+")
	print("Welcome to Apollo Marketplace.\nIt's like Amazon but for books.")
	authType = input("You want to login or signup ").lower()
	print("+-----------------------------------------------------------------+\n")

	if(authType == 'login'):
		login()
	elif(authType == 'signup'):
		signup()

main()
