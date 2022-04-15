from tkinter import *
from tkinter import ttk, messagebox
from tkinter import simpledialog
from PIL import ImageTk, Image
import mysql.connector as mycon
mydb = mycon.connect(host="localhost", user="root", password="", database="apollodb")
mycur = mydb.cursor()

auth = [] # To save users credentials such as user ID
cur_user_name = ""

root = Tk()
root.title("Apollo Marketplace")
root.geometry("1138x640")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

homeFrame          = Frame(root, bg="white")
buyerFrame         = Frame(root, bg="yellow")
sellerFrame        = Frame(root, bg="green")
productDetailFrame = Frame(root, bg="cyan")
thankYouFrame = Frame(root, bg="pink")
cartFrame = Frame(root, bg="light green")
showReviewsFrame = Frame(root, bg="orange")
writeReviewFrame = Frame(root, bg="blue")
addProductFrame = Frame(root, bg="brown")
viewStocksFrame = Frame(root, bg="gold")
viewReviewFrame = Frame(root, bg="purple")

for frame in (homeFrame, buyerFrame, sellerFrame, productDetailFrame, thankYouFrame, cartFrame, showReviewsFrame, writeReviewFrame, addProductFrame, viewStocksFrame, viewReviewFrame):
	frame.grid(row=0, column=0, sticky="nsew")

homeBgImage = PhotoImage(file = "images/home.jpg")
buyerBgImage = PhotoImage(file = "images/buyer.png")
sellerBgImage = PhotoImage(file = "images/seller.jpg")

Label(homeFrame, image = homeBgImage).place(relwidth = 1, relheight = 1)

Label(buyerFrame, image = buyerBgImage).place(relwidth = 1, relheight = 1)
Label(productDetailFrame, image = buyerBgImage).place(relwidth = 1, relheight = 1)
Label(thankYouFrame, image = buyerBgImage).place(relwidth = 1, relheight = 1)
Label(cartFrame, image = buyerBgImage).place(relwidth = 1, relheight = 1)
Label(showReviewsFrame, image = buyerBgImage).place(relwidth = 1, relheight = 1)
Label(writeReviewFrame, image = buyerBgImage).place(relwidth = 1, relheight = 1)

Label(sellerFrame, image = sellerBgImage).place(relwidth = 1, relheight = 1)
Label(addProductFrame, image = sellerBgImage).place(relwidth = 1, relheight = 1)
Label(viewStocksFrame, image = sellerBgImage).place(relwidth = 1, relheight = 1)
Label(viewReviewFrame, image = sellerBgImage).place(relwidth = 1, relheight = 1)

def show_frame(frame):
	frame.tkraise()
	print(frame)

def getAuth(email, password, authType):
	if(authType == 'buyer'):
		sql = ("SELECT userId, name from users WHERE email=%s AND password=%s")
		val = (email, password)
		mycur.execute(sql, val)

		res = mycur.fetchall()

		if(res == []):
			print("User does not exists.")
		else:
			auth.append(res[0][0]) # Selecting User ID
			auth.append(res[0][1])
			buyer()
	elif(authType == 'seller'):
		sql = ("SELECT sellerId, name from sellers WHERE email=%s AND password=%s")
		val = (email, password)
		mycur.execute(sql, val)

		res = mycur.fetchall()

		if(res == []):
			print("User does not exists.")
		else:
			auth.append(res[0][0]) # Selecting User ID
			auth.append(res[0][1])
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

def login():
	print(log_email.get())
	if(log_email.get()=="" or log_pass.get()==""):
		messagebox.showerror("Error", "All fields are required.")
	else:
		email = log_email.get()
		password = log_pass.get()
		question = messagebox.askquestion("Signup Type", "Signup as Buyer(Yes) or Signup as Buyer(No)")
		if(question=="yes"):
			loginType = "buyer"
		elif(question=="no"):
			loginType = "seller"
		
		UserExists = userExists(email, password, loginType)

		if(UserExists == True):
			getAuth(email, password, loginType)
		else:
			messagebox.showerror("Error", "Your entered email or password is incorrect.")

def register():
	print(reg_fname.get())
	if(reg_fname.get()=="" or reg_lname.get()=="" or reg_email.get()=="" or reg_pass.get()==""):
		messagebox.showerror("Error", "All fields are required.")
	elif(var_chk.get()==0):
		messagebox.showerror("Error", "You have not agreed to the terms and conditions.")
	else:
		name = reg_fname.get() + " " + reg_lname.get()
		email = reg_email.get()
		password = reg_pass.get()

		question = messagebox.askquestion("Signup Type", "Signup as Buyer(Yes) or Signup as Buyer(No)")
		if(question=="yes"):
			#Buyer
			sql = ("SELECT userId FROM users WHERE email=%s")
			val = (email,)
			mycur.execute(sql, val)
			res = mycur.fetchall()
			if(res == []):
				sql = ("INSERT into users(name, email, password) values(%s, %s, %s)")
				val = (name, email, password)
				mycur.execute(sql, val)
				mydb.commit()

				signupType = "buyer"
				getAuth(email, password, signupType)
			else:
				messagebox.showerror("Error", "Email is already in use.")
		elif(question=="no"):
			#Seller
			sql = ("SELECT sellerId FROM sellers WHERE email=%s")
			val = (email,)
			mycur.execute(sql, val)
			res = mycur.fetchall()
			if(res == []):
				sql = ("INSERT into sellers(name, email, password) values(%s, %s, %s)")
				val = (name, email, password)
				mycur.execute(sql, val)
				mydb.commit()

				signupType = "seller"
				getAuth(email, password, signupType)
			else:
				messagebox.showerror("Error", "Email is already in use.")

def logout():
	lout = messagebox.askquestion("Logout", "Do you really want to log out?")
	if(lout == 'yes'):
		auth.clear()
		show_frame(homeFrame)

def buyer():
	welcome = Label(buyerFrame, text="Hello, " + auth[1] , font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)
	show_frame(buyerFrame)


def showDetails(productId):
	show_frame(productDetailFrame)
	for widget in productDetFrame.winfo_children():
		widget.destroy()

	sql = ("SELECT products.productId, products.name, products.description, products.price, sellers.name FROM products LEFT JOIN sellers ON products.seller=sellers.sellerId WHERE products.productId=%s")
	val = (productId,)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	starRating = 0
	ratingCount = 0
	sql = ("SELECT rating from ratings WHERE product=%s")
	val = (productId,)
	mycur.execute(sql, val)
	ratRes = mycur.fetchall()
	if(ratRes == []):
		finalRating = 0
	else:
		for rating in ratRes:
			starRating = starRating + rating[0]
			ratingCount = ratingCount + 1
		finalRating = starRating/(ratingCount)

	if(res == []):
		messagebox.showerror("Error", "Something went wrong")
	else:
		for index, x in enumerate(res):
			num = 0
			productName = Label(productDetFrame, text=x[1], font=("calibri", 18, "bold"), bg="light gray").place(x=10, y=10)
			if(finalRating > 0):
				productRating = Label(productDetFrame, text=str(finalRating) + " star rating out of " + str(ratingCount) + " reviews", font=("calibri", 12, "bold"), bg="light gray").place(x=10, y=50)
			else:
				productRating = Label(productDetFrame, text="No one has rated this product yet.", font=(18)).place(x=10, y=50)
			productSeller = Label(productDetFrame, text="Seller - " + x[4], font=("calibri", 12, "bold"), bg="light gray").place(x=10, y=90)
			productDescription = Label(productDetFrame, text=x[2], bg="light gray").place(x=10, y=130)
			productPrice = Label(buyoutFrame, text="$" + str(x[3]), font=("calibri", 24), bg="light gray").place(x=10, y=10)

			showReviews_btn = Button(buyoutFrame, text="Show Reviews", command=lambda:showReviews(x[0])).place(x=10, y=60, width=120)
			addToCart_btn = Button(buyoutFrame, text="Add To Cart", command=lambda:addToCart(x[0])).place(x=10, y=100, width=120)
			buy_btn = Button(buyoutFrame, text="Buy Now", command=lambda:buyProduct(x[0], 'search')).place(x=10, y=140, width=120)

def addToCart(productId):
	sql = ("INSERT INTO cart(product, owner) values(%s, %s)")
	val = (productId, auth[0])
	mycur.execute(sql, val)
	mydb.commit()

	messagebox.showinfo("Success", "Product added to your cart successfully.")

def showReviews(productId):
	show_frame(showReviewsFrame)
	for widget in reviewProductFrame.winfo_children():
		widget.destroy()

	sql = ("SELECT users.name, reviews.review FROM reviews LEFT JOIN users ON users.userId=reviews.reviewBy WHERE product=%s")
	val = (productId,)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res == []):
		noReview = Label(reviewProductFrame, text="No one has reviewd this product yet.", font=("calibri", 18, "bold"), bg="light gray", pady=40).pack()
	else:
		for index, x in enumerate(res):
			num = 0
			reviewUsername = Label(reviewProductFrame, text=x[0] + " -", font=("calibri", 14, "bold"), bg="light gray").grid(row=index, column=num, pady=10)
			reviewDescription = Label(reviewProductFrame, text=x[1], font=("calibri", 14), bg="light gray").grid(row=index, column=num+1, pady=10, padx=10)

	showDetails_btn = Button(reviewHeaderFrame, text="Product Details", command=lambda:showDetails(productId)).place(x=960, y=18)
	addReview_btn = Button(buyProductFrame, text="Write a Review", command=lambda:writeReview(productId)).place(x=10, y=60, width=120)
	addToCart_btn = Button(buyProductFrame, text="Add To Cart", command=lambda:addToCart(productId)).place(x=10, y=100, width=120)
	buy_btn = Button(buyProductFrame, text="Buy Now", command=lambda:buyProduct(productId, 'search')).place(x=10, y=140, width=120)

def writeReview(productId):
	show_frame(writeReviewFrame)

	backToReview_btn = Button(writeReviewHeaderFrame, text="Reviews", command=lambda:showReviews(productId)).place(x=1000, y=18, width=60)
	reviewBox_btn = Button(writeReviewEntryFrame, text="Write Review", command=lambda:addReview(productId)).place(x=10, y=160, width=120)

def addReview(productId):
	ratingAdded = clicked.get()
	reviewAdded = reviewBox_e.get()

	if(reviewAdded != ""):
		sql = ("SELECT reviewId FROM reviews WHERE product=%s AND reviewBy=%s")
		val = (productId, auth[0])
		mycur.execute(sql, val)
		res = mycur.fetchall()
		if(res == []):
			sql = ("INSERT INTO reviews(review, product, reviewBy) values(%s, %s, %s)")
			val = (reviewAdded, productId, auth[0])
			mycur.execute(sql, val)
			mydb.commit()
		elif(res != []):
			sql = ("UPDATE reviews SET review=%s WHERE product=%s AND reviewBy=%s")
			val = (reviewAdded, productId, auth[0])
			mycur.execute(sql, val)
			mydb.commit()

	sql = ("SELECT ratingId FROM ratings WHERE product=%s AND ratingBy=%s")
	val = (productId, auth[0])
	mycur.execute(sql, val)
	res = mycur.fetchall()
	if(res == []):
		sql = ("INSERT INTO ratings(rating, product, ratingBy) values(%s, %s, %s)")
		val = (ratingAdded, productId, auth[0])
		mycur.execute(sql, val)
		mydb.commit()
	elif(res != []):
		sql = ("UPDATE ratings SET rating=%s WHERE product=%s AND ratingBy=%s")
		val = (ratingAdded, productId, auth[0])
		mycur.execute(sql, val)
		mydb.commit()

	messagebox.showinfo("Success", "Your review has been submitted")

def buyProduct(productId, history):
	if(history != "search"):
		print(history)
		sql = ("DELETE FROM cart WHERE productId = %s")
		val = (history,)
		mycur.execute(sql, val)
		mydb.commit()

	sql = ("INSERT INTO sales(product, boughtBy) values(%s, %s)")
	val = (productId, auth[0])
	mycur.execute(sql, val)
	mydb.commit()

	sql = ("UPDATE products SET stock=stock-1 WHERE productId=%s")
	val = (productId,)
	mycur.execute(sql, val)
	mydb.commit()

	show_frame(thankYouFrame)

def search():
	for widget in productFrame.winfo_children():
		widget.destroy()
	productName = search_entry.get()

	sql = ("SELECT products.productId, products.name, products.price, sellers.name, products.stock FROM products LEFT JOIN sellers ON products.seller=sellers.sellerId WHERE products.name=%s ORDER BY products.price ASC")
	val = (productName,)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res == []):
		noSearchResult = Label(productFrame, text="No such product exist on this marketplace.").pack()
	else:
		for index, x in enumerate(res):
			num = 0
			switch = x[0]
			image = PhotoImage(file = "users/products/pen.jpg")
			productImage = Label(productFrame, image=image, width=100, height=100).grid(row=index, column=num, pady=10, padx=10)
			productName = Label(productFrame, text=x[1], font=("calibri", 14, "bold"), bg="light gray").grid(row=index, column=num+1, pady=10, padx=10)
			productSeller = Label(productFrame, text="Seller - " + x[3], font=("calibri", 14), bg="light gray").grid(row=index, column=num+2, pady=10, padx=(40,10))
			productPrice = Label(productFrame, text="$" + str(x[2]), font=("calibri", 14), bg="light gray").grid(row=index, column=num+3, pady=10, padx=(160, 40))
			viewDetailsBtn = Button(productFrame, text="View Details", command=lambda switch=switch: showDetails(switch)).grid(row=index, column=num+5, pady=10)
def viewCart():
	show_frame(cartFrame)

	for widget in cartProductFrame.winfo_children():
		widget.destroy()

	for widget in buyCartFrame.winfo_children():
		widget.destroy()

	cartPrice = 0

	sql = ("SELECT cart.productId, products.productId, products.name, products.price, sellers.name FROM cart LEFT JOIN products ON products.productId=cart.product RIGHT JOIN sellers ON sellers.sellerId=products.seller WHERE owner=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res == []):
		noProductInCart = Label(cartProductFrame, text="Your cart doesnt have any product in it.", font=("calibri", 18, "bold"), bg="light gray", pady=40).pack()
	else:
		for index, x in enumerate(res):
			num = 0
			price = str(x[3])
			image = PhotoImage(file = "users/products/pen.jpg")
			productImage = Label(cartProductFrame, image=image, width=100, height=100).grid(row=index, column=num, pady=10, padx=10)
			cartProductName = Label(cartProductFrame, text=x[2], font=(24), bg="light gray").grid(row=index, column=num+1, pady=10, padx=10)
			cartProductSeller = Label(cartProductFrame, text="Seller - " + x[4], font=(18), bg="light gray").grid(row=index, column=num+2, pady=10, padx=(40, 10))
			cartProductPrice = Label(cartProductFrame, text=price, font=(24), bg="light gray").grid(row=index, column=num+3, pady=10, padx=(160, 40))
			cartBuyNow_btn = Button(cartProductFrame, text="Buy Now", command=lambda:buyProduct(x[0], x[0])).grid(row=index, column=num+5)
			cartPrice += x[3]
	
	title = Label(buyCartFrame, text="Buyout the cart", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)
	cartTotalPrice = Label(buyCartFrame, text="Cart = $" + str(cartPrice), font=("calibri", 18, "bold"), bg="light gray").place(x=10, y=80)
	buyout_btn = Button(buyCartFrame, text="Buy Out", command=buyoutCart).place(x=10, y=120)

def buyoutCart():
	sql = ("SELECT cart.productId, products.productId FROM cart LEFT JOIN products ON products.productId=cart.product WHERE owner=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res == []):
		messagebox.showerror("Error", "You dont have an product in your cart.")
	else:
		for x in res:
			buyProduct(x[1], x[0])

def seller():
	welcome = Label(sellerFrame, text="Hello, " + auth[1] , font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)
	show_frame(sellerFrame)

	salesToday = Label(salesReviewFrame, text="Sales today", font=("calibri", 18, "bold"), bg="light gray").place(x=10, y=60)
	
	sql = ("SELECT products.price FROM products LEFT JOIN sales ON sales.product = products.productId WHERE day(boughtOn)=day(curDate()) AND products.seller=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res != []):
		sold = 0
		for i in res:
			sold = sold + i[0]
		salesTodayFig = Label(salesReviewFrame, text="We sold product worth of " + str(sold) + " rupees today.", font=("calibri", 14), bg="light gray").place(x=10, y=90)
	elif(res == []):
		salesTodayFig = Label(salesReviewFrame, text="No product was sold today.", font=("calibri", 14), bg="light gray").place(x=10, y=90)
	
	salesToday = Label(salesReviewFrame, text="Sales from last 7 days", font=("calibri", 18, "bold"), bg="light gray").place(x=10, y=140)
	
	sql = ("SELECT products.price FROM products LEFT JOIN sales ON sales.product = products.productId WHERE week(boughtOn)=week(curDate()) AND products.seller=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()
	print(res)
	if(res != []):
		sold = 0
		for i in res:
			sold = sold + i[0]
		salesTodayFig = Label(salesReviewFrame, text="We sold product worth of " + str(sold) + " rupees this week.", font=("calibri", 14), bg="light gray").place(x=10, y=170)
	elif(res == []):
		sold = 0
		for i in res:
			sold = sold + i[0]
		salesTodayFig = Label(salesReviewFrame, text="No product was sold this week.", font=("calibri", 14), bg="light gray").place(x=10, y=170)
	
	salesToday = Label(salesReviewFrame, text="Sales from last 30 days", font=("calibri", 18, "bold"), bg="light gray").place(x=10, y=220)
	
	sql = ("SELECT products.price FROM products LEFT JOIN sales ON sales.product = products.productId WHERE month(boughtOn)=month(curDate()) AND products.seller=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()
	print(res)
	if(res != []):
		sold = 0
		for i in res:
			sold = sold + i[0]
		salesTodayFig = Label(salesReviewFrame, text="We sold product worth of " + str(sold) + " rupees this month", font=("calibri", 14), bg="light gray").place(x=10, y=250)
	elif(res == []):
		sold = 0
		for i in res:
			sold = sold + i[0]
		salesTodayFig = Label(salesReviewFrame, text="No product was sold this month.", font=("calibri", 14), bg="light gray").place(x=10, y=250)

	sql = ("SELECT COUNT(productId) FROM products WHERE seller=%s AND stock<10")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res[0][0] > 0):
		stocksFig = Label(reviewExtrasFrame, text=str(res[0][0]) + " products have low stocks.", font=("calibri", 12, "bold"), bg="light gray").place(x=10, y=60)
	elif(res[0][0] == 0):
		stocksFig = Label(reviewExtrasFrame, text="Your stock are upto demand.", font=("calibri", 12, "bold"), bg="light gray").place(x=10, y=60)

	sql = ("SELECT ratings.rating FROM products LEFT JOIN ratings ON ratings.product = products.productId WHERE products.seller=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	print("Ratings", res)
	
	if(res[0][0] == None):
		ratingsFig = Label(reviewExtrasFrame, text="You don't have any reviews.", font=("calibri", 12, "bold"), bg="light gray").place(x=10, y=170)
	elif(res != []):
		rating = 0
		ratingCount = 0
		for i in res:
			if(i[0] != None):
				rating = rating + i[0]
				ratingCount += 1

		rating = rating/ratingCount
		if(rating <= 5 and rating >= 4):
			ratings = "mostly positive."
		elif(rating <= 4 and rating >= 3):
			ratings = "positive."
		elif(rating <= 3 and rating >= 2):
			ratings = "negative."
		elif(rating <= 2 and rating >= 1):
			ratings = "mostly negative."

		ratingsFig = Label(reviewExtrasFrame, text="Your reviews are " + ratings, font=("calibri", 12, "bold"), bg="light gray").place(x=10, y=170)

def addProduct():
	show_frame(addProductFrame)

def addNewProduct():
	if(newProductName_e.get()=="" or newProductDescription_e.get()=="" or newProductPrice_e.get()=="" or newProductStock_e.get()==""):
		messagebox.showerror("Error", "All fields are required.")
	else:
		name = newProductName_e.get()
		description = newProductDescription_e.get()
		price = newProductPrice_e.get()
		stock = newProductStock_e.get()

		sql = ("INSERT INTO products(name, description, price, stock, seller) values(%s, %s, %s, %s, %s)")
		val = (name, description, price, stock, auth[0])
		mycur.execute(sql, val)
		mydb.commit()

		messagebox.showinfo("Success", "Product has been added to your catalog.")

		seller()

def viewStocks():
	show_frame(viewStocksFrame)

	for widget in stockProductsFrame.winfo_children():
		widget.destroy()

	sql = ("SELECT productId, name, price, stock FROM products WHERE seller=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res == []):
		noProductResult = Label(stockProductsFrame, text="You don't have any product in your catalog.").pack()
	else:
		for index, x in enumerate(res):
			num = 0
			product = x[0]
			image = PhotoImage(file = "users/products/pen.jpg")
			productImage = Label(stockProductsFrame, image=image, width=100, height=100).grid(row=index, column=num, pady=10, padx=10)
			productName = Label(stockProductsFrame, text=x[1], font=("calibri", 14, "bold"), bg="light gray").grid(row=index, column=num+1, pady=10, padx=20)
			productPrice = Label(stockProductsFrame, text="$" + str(x[2]), font=("calibri", 14), bg="light gray").grid(row=index, column=num+2, pady=10, padx=20)
			productStock = Label(stockProductsFrame, text=str(x[3]) + " stock left", font=("calibri", 14), bg="light gray").grid(row=index, column=num+3, pady=10, padx=(180, 60))
			addStockBtn = Button(stockProductsFrame, text="Add Stocks", command=lambda product=product: addStocks(product)).grid(row=index, column=num+5, pady=10)

def addStocks(productId):
	print(productId)
	amount = simpledialog.askinteger("Input", "How much stock you want to add?", parent=root, minvalue=0, maxvalue=1000)

	if(amount == 0):
		messagebox.showerror("Error", "Enter some kind of value.")
	elif(amount > 0):
		sql = ("UPDATE products SET stock=stock+%s WHERE productId=%s AND seller=%s")
		val = (amount, productId, auth[0])
		mycur.execute(sql, val)
		mydb.commit()

		messagebox.showinfo("Success", "Successfully added stock.")
		viewStocks()

def viewReviews():
	show_frame(viewReviewFrame)

	for widget in reviewProductsFrame.winfo_children():
		widget.destroy()

	sql = ("SELECT productId, name FROM products WHERE seller=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	for i in res:
		sql = ("SELECT users.name, reviews.review FROM reviews LEFT JOIN users ON users.userId=reviews.reviewBy WHERE product=%s")
		val = (i[0],)
		mycur.execute(sql, val)
		res = mycur.fetchall()

		if(res == []):
			noReviewResult = Label(stockProductsFrame, text="No one has written reviews to your products yet.").pack()
		else:
			for index, x in enumerate(res):
				num = 0
				reviewBuyerProductName = Label(reviewProductsFrame, text="On product '" + i[1] + "'", font=("calibri", 14, "bold"), bg="light gray").grid(row=index, column=num, pady=10, padx=20)
				reviewBuyerUsername = Label(reviewProductsFrame, text=x[0] + ":", font=("calibri", 12, "bold"), bg="light gray").grid(row=index, column=num+1, pady=10, padx=10)
				reviewBuyerDescription = Label(reviewProductsFrame, text='"' + x[1] + '"', font=("calibri", 12), bg="light gray").grid(row=index, column=num+2, pady=10,)

loginFrame=Frame(homeFrame, bg="light gray")
loginFrame.place(x=0, y=0, width=1138, height=70)

title = Label(loginFrame, text="Appolo Marketplace", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)

email = Label(loginFrame, text="Email", font=("calibri", 14), bg="light gray").place(x=600, y=18)
log_email = Entry(loginFrame, font=("calibri", 12), bg="gray")
log_email.place(x=650, y=18, width=150)

password = Label(loginFrame, text="Password", font=("calibri", 14), bg="light gray").place(x=820, y=18)
log_pass = Entry(loginFrame, font=("calibri", 12), bg="gray")
log_pass.place(x=906, y=18, width=150)

login_btn = Button(loginFrame, text="Login", command=login).place(x=1070, y=18, width=60)

signupFrame=Frame(homeFrame, bg="light gray")
signupFrame.place(x=680, y=100, width=400, height=330)

title = Label(signupFrame, text="Register", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)
        
fname = Label(signupFrame, text="First Name", font=("calibri", 14), bg="light gray").place(x=10, y=80)
reg_fname = Entry(signupFrame, font=("calibri", 12), bg="gray")
reg_fname.place(x=110, y=80, width=150)

lname = Label(signupFrame, text="Last Name", font=("calibri", 14), bg="light gray").place(x=10, y=120)
reg_lname = Entry(signupFrame, font=("calibri", 12), bg="gray")
reg_lname.place(x=110, y=120, width=150)

email = Label(signupFrame, text="Email", font=("calibri", 14), bg="light gray").place(x=10, y=160)
reg_email = Entry(signupFrame, font=("calibri", 12), bg="gray")
reg_email.place(x=110, y=160, width=150)

password = Label(signupFrame, text="Password", font=("calibri", 14), bg="light gray").place(x=10, y=200)
reg_pass = Entry(signupFrame, font=("calibri", 12), bg="gray")
reg_pass.place(x=110, y=200, width=150)

var_chk = IntVar()
check = Checkbutton(signupFrame, text="I agree to the Terms & Conditions", variable=var_chk, onvalue=1, offvalue=0, font=("calibri", 14), bg="light gray")
check.place(x=10, y=240)

signup_btn = Button(signupFrame, text="Create Account", command=register).place(x=10, y=280, width=120)


#Buyer Frame
headerFrame=Frame(buyerFrame, bg="light gray")
headerFrame.place(x=0, y=0, width=1138, height=70)

cart_btn = Button(buyerFrame, text="Cart", command=viewCart).place(x=1000, y=18, width=60)
logout_btn = Button(buyerFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

productFrame=Frame(buyerFrame, bg="light gray")
productFrame.place(x=60, y=100, width=720, height=540)

searchFrame=Frame(buyerFrame, bg="light gray")
searchFrame.place(x=840, y=100, width=240, height=330)

search_entry = Entry(searchFrame, font=("calibri", 12), bg="gray")
search_entry.place(x=10, y=20, width=150)

search_btn = Button(searchFrame, text="Search", command=search).place(x=10, y=60, width=120)


#Show Details Frame
headerFrame=Frame(productDetailFrame, bg="light gray")
headerFrame.place(x=0, y=0, width=1138, height=70)

home_btn = Button(headerFrame, text="Home", command=buyer).place(x=930, y=18, width=60)
cart_btn = Button(headerFrame, text="Cart", command=viewCart).place(x=1000, y=18, width=60)
logout_btn = Button(headerFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

productDetFrame=Frame(productDetailFrame, bg="light gray")
productDetFrame.place(x=60, y=100, width=720, height=540)



buyoutFrame=Frame(productDetailFrame, bg="light gray")
buyoutFrame.place(x=840, y=100, width=240, height=330)

#Thank you Frame
headerFrame=Frame(thankYouFrame, bg="light gray")
headerFrame.place(x=0, y=0, width=1138, height=70)

home_btn = Button(headerFrame, text="Home", command=buyer).place(x=930, y=18, width=60)
cart_btn = Button(headerFrame, text="Cart", command=viewCart).place(x=1000, y=18, width=60)
logout_btn = Button(headerFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

thankYouNoteFrame=Frame(thankYouFrame, bg="light gray")
thankYouNoteFrame.place(x=60, y=100, width=1015, height=540)

thankYouNote = Label(thankYouNoteFrame, text="Thank you, for shopping with us.", font=("calibri", 36, "bold"), bg="light gray")
thankYouNote.pack()

continue_btn = Button(thankYouNoteFrame, text="Continue Shopping", command=buyer)
continue_btn.pack()


#Cart Frame

headerFrame=Frame(cartFrame, bg="light gray")
headerFrame.place(x=0, y=0, width=1138, height=70)

home_btn = Button(headerFrame, text="Home", command=buyer).place(x=1000, y=18, width=60)
logout_btn = Button(headerFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

cartProductFrame=Frame(cartFrame, bg="light gray")
cartProductFrame.place(x=60, y=100, width=720, height=540)

buyCartFrame=Frame(cartFrame, bg="light gray")
buyCartFrame.place(x=840, y=100, width=240, height=330)

#Review Frame

reviewHeaderFrame=Frame(showReviewsFrame, bg="light gray")
reviewHeaderFrame.place(x=0, y=0, width=1138, height=70)

logout_btn = Button(reviewHeaderFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

reviewProductFrame=Frame(showReviewsFrame, bg="light gray")
reviewProductFrame.place(x=60, y=100, width=720, height=540)

buyProductFrame=Frame(showReviewsFrame, bg="light gray")
buyProductFrame.place(x=840, y=100, width=240, height=330)

#Write Review Frame

writeReviewHeaderFrame=Frame(writeReviewFrame, bg="light gray")
writeReviewHeaderFrame.place(x=0, y=0, width=1138, height=70)

logout_btn = Button(writeReviewHeaderFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

writeReviewEntryFrame=Frame(writeReviewFrame, bg="light gray")
writeReviewEntryFrame.place(x=60, y=100, width=1020, height=330)

title = Label(writeReviewEntryFrame, text="Write Review", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)

reviewBox = Label(writeReviewEntryFrame, text="Review", font=("calibri", 14), bg="light gray").place(x=10, y=80)
reviewBox_e = Entry(writeReviewEntryFrame, font=("calibri", 12), bg="gray")
reviewBox_e.place(x=110, y=80, width=150)

rating_l = Label(writeReviewEntryFrame, text="Rating", font=("calibri", 14), bg="light gray").place(x=10, y=120)
clicked = StringVar()
clicked.set(1)
rating_e = OptionMenu(writeReviewEntryFrame, clicked, 1, 2, 3, 4, 5).place(x=110, y=120)

#Seller Frame

headerFrame=Frame(sellerFrame, bg="light gray")
headerFrame.place(x=0, y=0, width=1138, height=70)

cart_btn = Button(sellerFrame, text="Add Product", command=addProduct).place(x=980, y=18)
logout_btn = Button(sellerFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

salesReviewFrame=Frame(sellerFrame, bg="light gray")
salesReviewFrame.place(x=60, y=100, width=720, height=330)
title = Label(salesReviewFrame, text="Sales Review", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)

reviewExtrasFrame=Frame(sellerFrame, bg="light gray")
reviewExtrasFrame.place(x=840, y=100, width=240, height=330)

title = Label(reviewExtrasFrame, text="Stocks", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)
showBuyerStocks_btn = Button(reviewExtrasFrame, text="View Stocks", command=viewStocks).place(x=10, y=90)

title = Label(reviewExtrasFrame, text="Reviews", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=120)
showBuyerReviews_btn = Button(reviewExtrasFrame, text="View Reviews", command=viewReviews).place(x=10, y=200)

#Add Product Frame

headerFrame=Frame(addProductFrame, bg="light gray")
headerFrame.place(x=0, y=0, width=1138, height=70)

home_btn = Button(headerFrame, text="Home", command=seller).place(x=1000, y=18, width=60)
logout_btn = Button(addProductFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

addProductEntryFrame=Frame(addProductFrame, bg="light gray")
addProductEntryFrame.place(x=60, y=100, width=1020, height=330)

title = Label(addProductEntryFrame, text="Add Product", font=("calibri", 24, "bold"), bg="light gray").place(x=10, y=10)
        
newProductName = Label(addProductEntryFrame, text="Name", font=("calibri", 14), bg="light gray").place(x=10, y=80)
newProductName_e = Entry(addProductEntryFrame, font=("calibri", 12), bg="gray")
newProductName_e.place(x=110, y=80, width=150)

newProductDescription = Label(addProductEntryFrame, text="Description", font=("calibri", 14), bg="light gray").place(x=10, y=120)
newProductDescription_e = Entry(addProductEntryFrame, font=("calibri", 12), bg="gray")
newProductDescription_e.place(x=110, y=120, width=150)

newProductPrice = Label(addProductEntryFrame, text="Price", font=("calibri", 14), bg="light gray").place(x=10, y=160)
newProductPrice_e = Entry(addProductEntryFrame, font=("calibri", 12), bg="gray")
newProductPrice_e.place(x=110, y=160, width=150)

newProductStock = Label(addProductEntryFrame, text="Stock", font=("calibri", 14), bg="light gray").place(x=10, y=200)
newProductStock_e = Entry(addProductEntryFrame, font=("calibri", 12), bg="gray")
newProductStock_e.place(x=110, y=200, width=150)

addNewProduct_btn = Button(addProductEntryFrame, text="Create Product", command=addNewProduct).place(x=10, y=240, width=120)

#View Stock Frame

headerFrame=Frame(viewStocksFrame, bg="light gray")
headerFrame.place(x=0, y=0, width=1138, height=70)

home_btn = Button(headerFrame, text="Home", command=seller).place(x=1000, y=18, width=60)
logout_btn = Button(viewStocksFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

stockProductsFrame=Frame(viewStocksFrame, bg="light gray")
stockProductsFrame.place(x=60, y=100, width=1020, height=540)

#View Review Frame

headerFrame=Frame(viewReviewFrame, bg="light gray")
headerFrame.place(x=0, y=0, width=1138, height=70)

home_btn = Button(headerFrame, text="Home", command=seller).place(x=1000, y=18, width=60)
logout_btn = Button(viewReviewFrame, text="Logout", command=logout).place(x=1070, y=18, width=60)

reviewProductsFrame=Frame(viewReviewFrame, bg="light gray")
reviewProductsFrame.place(x=60, y=100, width=1020, height=540)

show_frame(homeFrame)

root.mainloop()