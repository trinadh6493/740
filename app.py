from flask import Flask, Response, request, render_template, redirect
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
    db = mongo.ecommerce
    mongo.server_info()
except:
    print("Error: Cannot connect to the database")


@app.route("/", methods=["GET"])

def index():
    users = list(db.users.find())
    for user in users:
        user["_id"] = str(user["_id"])
    stock = list(db.stock.find())
    for stoc in stock:
        stoc["_id"]=str(stoc["_id"])
    products = list(db.products.find())
    for product in products:
        product["_id"] = str(product["_id"])
    purchases = list(db.purchases.find())
    for purchase in purchases:
        purchase["_id"] = str(purchase["_id"])
    return render_template("index.html", users=users, products=products, stock=stock, purchases=purchases)

    


@app.route("/users", methods=["POST"])
def create_user():
    try:
        method = request.form["_method"]
        if method == "PATCH":
            return update_user(request.form["id"])
        elif method == "DELETE":
            return delete_user(request.form["id"])
    except KeyError:
        pass

    try:
        user = {"firstName": request.form["firstName"], "lastName": request.form["lastName"]}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
    except Exception as ex:
        print(ex)

    return redirect("/")

    # Handle the create user request here
@app.route("/users/<id>", methods=["POST"])
def update_user(id):
    print(f"Updating user with ID: {id}")
    user = db.users.find_one({"_id": ObjectId(id)})
    if user:
        try:
            firstName = request.form.get("firstName")
            if firstName:
                dbResponse = db.users.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": {"firstName": firstName}},
                )
                if dbResponse.modified_count == 1:
                    return redirect("/")
                else:
                    return Response(
                        response=json.dumps({"message": "nothing to update"}),
                        status=200,
                        mimetype="application/json",
                    )
            else:
                return Response(
                    response=json.dumps({"message": "missing parameter: firstName"}),
                    status=400,
                    mimetype="application/json",
                )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({"message": "cannot update users data"}),
                status=500,
                mimetype="application/json",
            )
    else:
        print(f"User with ID {id} not found")
        return Response(
            response=json.dumps({"message": "User not found"}),
            status=404,
            mimetype="application/json",
        )





@app.route("/delete_user/<id>", methods=["POST"])
def delete_user(id):
    print("Aaaaa")
    print(request.method)
    if request.method == "POST":
        # Handle delete action
        print("Aaaaa")
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        print("Bbbbb")
        if dbResponse.deleted_count == 1:
            print("Bbbbb")
            return redirect("/")
        else:
            return Response(
                response=json.dumps({"message": "User not found"}),
                status=404,
                mimetype="application/json",
            )
    else:
        # Invalid HTTP method
        return Response(
            response=json.dumps({"message": "Invalid HTTP method"}),
            status=405,
            mimetype="application/json",
        )


@app.route("/products", methods=["POST"])
def create_product():
    try:
        method = request.form["_method"]
        if method == "PATCH":
            return update_product(request.form["id"])
        elif method == "DELETE":
            return delete_product(request.form["id"])
    except KeyError:
        pass

    try:
        product = {
            "productName": request.form["productName"],
            "productType": request.form["productType"],
            "productPrice": request.form["productPrice"]
        }
        stock = {
            "stockName": request.form["productName"],
            "stockQuantity": request.form["stockQuantity"]
        }
        
        dbResponseProduct = db.products.insert_one(product)
        product_id = str(dbResponseProduct.inserted_id)
        
        stock["product_id"] = product_id
        dbResponseStock = db.stock.insert_one(stock)
        stock_id = str(dbResponseStock.inserted_id)
        
        # Update the product document with the stock_id
        db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"stock_id": ObjectId(stock_id)}}
        )
        
        # Update the stock document with the product_id
        db.stock.update_one(
            {"_id": ObjectId(stock_id)},
            {"$set": {"product_id": ObjectId(product_id)}}
        )
        
        print(dbResponseProduct.inserted_id)
        print(dbResponseStock.inserted_id)
    except Exception as ex:
        print(ex)

    return redirect("/")




    # Handle the create user request here

@app.route('/stock', methods=['POST'])
def create_stock():
    try:
        method = request.form["_method"]
        if method == "PATCH":
            return update_stock(request.form["id"])
        elif method == "DELETE":
            return delete_stock(request.form["id"])
    except KeyError:
        pass

    try:
        stoc = {"stockName": request.form["stockName"], "stockQuantity": request.form["stockQuantity"]}
        dbResponse = db.stock.insert_one(stoc)
        print(dbResponse.inserted_id)
    except Exception as ex:
        print(ex)

    return redirect("/")



@app.route("/products/<id>", methods=["POST"])
def update_product(id):
    print(f"Updating product with ID: {id}")
    product = db.products.find_one({"_id": ObjectId(id)})
    if product:
        try:
            productName = request.form.get("productName")
            if productName:
                dbResponse = db.products.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": {"productName": productName}},
                )
                if dbResponse.modified_count == 1:
                    return redirect("/")
                else:
                    return Response(
                        response=json.dumps({"message": "nothing to update"}),
                        status=200,
                        mimetype="application/json",
                    )
            else:
                return Response(
                    response=json.dumps({"message": "missing parameter: productName"}),
                    status=400,
                    mimetype="application/json",
                )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({"message": "cannot update users data"}),
                status=500,
                mimetype="application/json",
            )
    else:
        print(f"User with ID {id} not found")
        return Response(
            response=json.dumps({"message": "User not found"}),
            status=404,
            mimetype="application/json",
        )

@app.route("/stock/<id>", methods=["POST"])
def update_stock(id):
    print(f"Updating product with ID: {id}")
    product = db.stock.find_one({"_id": ObjectId(id)})
    if product:
        try:
            stockQuantity = request.form.get("stockQuantity")
            if stockQuantity:
                dbResponse = db.stock.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": {"stockQuantity": stockQuantity}},
                )
                if dbResponse.modified_count == 1:
                    return redirect("/")
                else:
                    return Response(
                        response=json.dumps({"message": "nothing to update"}),
                        status=200,
                        mimetype="application/json",
                    )
            else:
                return Response(
                    response=json.dumps({"message": "missing parameter: stockQuantity"}),
                    status=400,
                    mimetype="application/json",
                )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({"message": "cannot update users data"}),
                status=500,
                mimetype="application/json",
            )
    else:
        print(f"User with ID {id} not found")
        return Response(
            response=json.dumps({"message": "User not found"}),
            status=404,
            mimetype="application/json",
        )


@app.route("/delete_product/<id>", methods=["POST"])
def delete_product(id):
    print("Aaaaa")
    print(request.method)
    if request.method == "POST":
        # Handle delete action
        print("Aaaaa")
        dbResponse = db.products.delete_one({"_id": ObjectId(id)})
        print("Bbbbb")
        if dbResponse.deleted_count == 1:
            print("Bbbbb")
            return redirect("/")
        else:
            return Response(
                response=json.dumps({"message": "User not found"}),
                status=404,
                mimetype="application/json",
            )
    else:
        # Invalid HTTP method
        return Response(
            response=json.dumps({"message": "Invalid HTTP method"}),
            status=405,
            mimetype="application/json",
        )

@app.route("/delete_stock/<id>", methods=["POST"])
def delete_stock(id):
    print("Aaaaa")
    print(request.method)
    if request.method == "POST":
        # Handle delete action
        print("Aaaaa")
        dbResponse = db.stock.delete_one({"_id": ObjectId(id)})
        print("Bbbbb")
        if dbResponse.deleted_count == 1:
            print("Bbbbb")
            return redirect("/")
        else:
            return Response(
                response=json.dumps({"message": "User not found"}),
                status=404,
                mimetype="application/json",
            )
    else:
        # Invalid HTTP method
        return Response(
            response=json.dumps({"message": "Invalid HTTP method"}),
            status=405,
            mimetype="application/json",
        )




@app.route("/purchase", methods=["POST"])
def create_purchase():
    try:
        user_id = request.form["user_id"]
        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])

        user = db.users.find_one({"_id": ObjectId(user_id)})
        product = db.products.find_one({"_id": ObjectId(product_id)})

        stock = db.stock.find_one({"product_id": ObjectId(product_id)})

        print("Stock Quantity:", stock["stockQuantity"])  # Move this line here
        print("Requested Quantity:", quantity)
        print(stock)

        if stock is None or int(stock["stockQuantity"]) < quantity:
            return Response(
                response=json.dumps({"message": "Insufficient stock"}),
                status=400,
                mimetype="application/json"
            )

        # Reduce the stock quantity
        new_quantity = int(stock["stockQuantity"]) - quantity
        db.stock.update_one(
            {"product_id": ObjectId(product_id)},
            {"$set": {"stockQuantity": new_quantity}}
        )

        # Create the purchase document
        purchase = {
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        }

        # Insert the purchase document into the purchase collection
        db.purchases.insert_one(purchase)

        return redirect("/")
    except KeyError:
        return Response(
            response=json.dumps({"message": "Missing required parameters"}),
            status=400,
            mimetype="application/json"
        )
    except ValueError:
        return Response(
            response=json.dumps({"message": "Invalid quantity value"}),
            status=400,
            mimetype="application/json"
        )

@app.route("/delete_purchase/<id>", methods=["POST"])
def delete_purchase(id):
    print("Aaaaa")
    print(request.method)
    if request.method == "POST":
        # Handle delete action
        print("Aaaaa")
        dbResponse = db.purchases.delete_one({"_id": ObjectId(id)})
        print("Bbbbb")
        if dbResponse.deleted_count == 1:
            print("Bbbbb")
            return redirect("/")
        else:
            return Response(
                response=json.dumps({"message": "User not found"}),
                status=404,
                mimetype="application/json",
            )
    else:
        # Invalid HTTP method
        return Response(
            response=json.dumps({"message": "Invalid HTTP method"}),
            status=405,
            mimetype="application/json",
        )



# ... other routes ...





if __name__ == "__main__":
    app.run(port=5000, debug=True)