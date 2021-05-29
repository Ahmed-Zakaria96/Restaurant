# Introduction

Restaurant Series web-app that allow users to order items and browse restaurants menus.

## Structure
the app is built using flask app in the backend with postgresql and html, css, bootstrap and js in the front end.
the app is hosted on heroku using the free plan [https://restaurantseriestask.herokuapp.com/](https://restaurantseriestask.herokuapp.com/)
1. "8" database models(User, Role, Series, Restaurant, Menu, MenuItems, Order, OrderItems)
2. "9" routes:
	- index: renders the home page ('index.html')
	- order: render order page('order.html')
	- submit_order: used to submit order via api
	- restaurants: used to get all restaurants via api
	- restaurants/id: used to get restaurant menu via api
	- register: renders register template ('register.html')
	- login: renders register template ('login.html')
	- apilogin: used for user login via api request
	- logout: used to clear session and log out user
