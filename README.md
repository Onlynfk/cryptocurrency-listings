# [Django Bitcoin Price listings using CoinMarketcap Api] 

- ✅ Responsive mobile first view
-.✅ Background tasks to populate Django database with new updates from coinmarketcap API every 5 mins
- ✅ Inline rows edit/delete activated at double click on coin data item
- ✅ Realtime Search functionality while typing
- ✅ Display graph in Django app database 
- ✅ MySql for django database 

<br />

![photo_5852645406641601603_w](https://user-images.githubusercontent.com/52893267/209423033-220b1444-c2e9-4ec6-962d-16a2cd93a672.jpg)

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/Onlynfk/cryptocurrency-listings.git
$ cd cryptocurrency-listings
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules -
$ pip3 install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Create app superuser
$ python manage.py createsuperuser
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/

$ # Start Schedule Job to Sync db from Coinmarketcap API 

```sh

$ python manange.py crontab add # adds the schedule job

$ python manange.py crontab show # show the schedule job

$ python manange.py crontab remove # remove the schedule job

```


