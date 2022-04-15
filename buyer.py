def home():
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
			productName = Label(productDetFrame, text=x[1], font=(28)).place(x=10, y=10)
			if(finalRating > 0):
				productRating = Label(productDetFrame, text=str(finalRating) + " star rating out of " + str(ratingCount) + " reviews", font=(18)).place(x=10, y=50)
			else:
				productRating = Label(productDetFrame, text="No one has rated this product yet.", font=(18)).place(x=10, y=50)
			productSeller = Label(productDetFrame, text="Seller - " + x[4], font=(18)).place(x=10, y=90)
			productDescription = Label(productDetFrame, text=x[2], font=(18)).place(x=10, y=130)
			productPrice = Label(buyoutFrame, text=x[3], font=(18)).place(x=10, y=10)

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

	sql = ("SELECT users.name, ratings.rating, reviews.review FROM reviews LEFT JOIN users ON reviews.reviewBy=users.userId RIGHT JOIN ratings ON reviews.reviewBy=ratings.ratingBy WHERE reviews.product=%s")
	val = (productId,)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res == []):
		noReview = Label(reviewProductFrame, text="No one has reviewd this product yet.").pack()
	else:
		for index, x in enumerate(res):
			num = 0
			reviewUsername = Label(reviewProductFrame, text=x[0], font=(24)).grid(row=index, column=num)
			reviewRating = Label(reviewProductFrame, text=str(x[1]), font=(18)).grid(row=index, column=num+1)
			reviewDescription = Label(reviewProductFrame, text=x[2], font=(24)).grid(row=index+1, column=num)

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
			productName = Label(productFrame, text=x[1], font=(24)).grid(row=index, column=num)
			productSeller = Label(productFrame, text="Seller - " + x[3], font=(18)).grid(row=index, column=num+1)
			productPrice = Label(productFrame, text=x[2], font=(24)).grid(row=index, column=num+2)
			viewDetailsBtn = Button(productFrame, text="View Details", command=lambda:showDetails(x[0])).grid(row=index, column=num+4)	

def viewCart():
	show_frame(cartFrame)

	for widget in cartProductFrame.winfo_children():
		widget.destroy()

	cartPrice = 0

	sql = ("SELECT cart.productId, products.productId, products.name, products.price, sellers.name FROM cart LEFT JOIN products ON products.productId=cart.product RIGHT JOIN sellers ON sellers.sellerId=cart.owner WHERE owner=%s")
	val = (auth[0],)
	mycur.execute(sql, val)
	res = mycur.fetchall()

	if(res == []):
		noProductInCart = Label(cartProductFrame, text="Your cart donesnt have any product in it.").pack()
	else:
		for index, x in enumerate(res):
			num = 0
			price = str(x[3])
			cartProductName = Label(cartProductFrame, text=x[2], font=(24)).grid(row=index, column=num)
			cartProductSeller = Label(cartProductFrame, text="Seller - " + x[4], font=(18)).grid(row=index, column=num+1)
			cartProductPrice = Label(cartProductFrame, text=price, font=(24)).grid(row=index, column=num+2)
			cartBuyNow_btn = Button(cartProductFrame, text="Buy Now", command=lambda:buyProduct(x[0], x[0])).grid(row=index, column=num+4)
			cartPrice += x[3]
	
	cartTotalPrice = Label(buyCartFrame, text="Price = " + str(cartPrice)).place(x=10, y=80)

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