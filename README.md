# My-vaccine
When the code has been written and you're satisfied write the following in the terminal:
cd My-vaccine

.\env\Scripts\activate  
cd backend
python manage.py makemigrations   
python manage.py migrate  
python manage.py runserver

System Administrator is in the Sysadmin app
In this app there is Facility admin,Abstractuser, Healthfacility and Vaccine listo
They simultaneously add the facility and its Admin and then they add the vaccines that the hospital has 
Here the System admin registers the Facility and allows them to change their password later once they log-in

The Sysadmin log-in API view Test was a success
"token":"444b8dc9c93d84051f8e8cd8d200da11100266d5","user_id":1,"username":"super","role":"SYSTEM_ADMIN","must_change_password":***-#false/true
#Second try
{"token":"32232a2f4f16509af84aa6e78f19b54a182b3b23","user_id":1,"username":"super","role":"SYSTEM_ADMIN","must_change_password":true}
#Third try
{"token":"e6bdc60b641cf6454f69c7480904832264ae60dd","user_id":1,"username":"super","role":"SYSTEM_ADMIN","must_change_password":true}

The System log-out API view Test was a succes
{"message":"Successfully logged out"}
#Second Try
{"message":"Successfully logged out"}

The System admin dashboard API VIEW test- Success
{"message":"Dashboard data"}