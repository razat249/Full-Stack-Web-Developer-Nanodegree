from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem



engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()





# List of restaurants
@app.route('/')
@app.route('/restaurants/')
@app.route('/index/')
def list_restaurants():
    all_restaurants = session.query(Restaurant).all()
    return render_template('list_restaurants.html', all_restaurants = all_restaurants)

# Add new Restaurant
@app.route('/restaurants/new/', methods = ['GET','POST'])
def new_restaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(name = request.form['name'])
        session.add(new_restaurant)
        session.commit()
        return redirect(url_for('list_restaurants'))
    else:
        return render_template('new_restaurant.html')

# Edit name of existing restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET','POST'])
def edit_restaurant(restaurant_id):
    if request.method == 'POST':
        restaurant_to_edit = session.query(Restaurant).filter_by(id = restaurant_id).one()
        if request.form['name']:
            restaurant_to_edit.name = request.form['name']
        session.add(restaurant_to_edit)
        session.commit()
        return redirect(url_for('list_restaurants'))
    else:
        return render_template('edit_restaurant.html', restaurant_id = restaurant_id)

# Delete the restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET','POST'])
def delete_restaurant(restaurant_id):
    if request.method == 'POST':
        restaurant_to_delete = session.query(Restaurant).filter_by(id = restaurant_id).one()
        session.delete(restaurant_to_delete)
        session.commit()
        return redirect(url_for('list_restaurants'))
    else:
        return render_template('delete_restaurant.html',restaurant_id = restaurant_id)









@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html',restaurant = restaurant, restaurant_id = restaurant_id, items = items)
    
# Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		new_item = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		session.add(new_item)
		session.commit()
                flash("New Menu Item Created!")        
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Menu Item edited!") 
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, i=editedItem)

# Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleted_item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(deleted_item)
        session.commit()
        flash("Menu Item deleted!")
        return redirect( url_for('restaurantMenu',restaurant_id = restaurant_id) )
    else:
        return render_template('deletemenuitem.html',item = deleted_item, restaurant_id = restaurant_id, menu_id = menu_id)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
