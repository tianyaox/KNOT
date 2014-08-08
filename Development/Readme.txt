
please follow the guide in package_install to install necessary package.

Make sure you activate virtualenv when you development!!!!111.


use python manage.py shell to generate dummy database
from dummyData import *
generateDummyData()



for the api local test

when test Facebook, change ROOT_URL in settings.py to http://localhost:8000/, other api works well in http://127.0.0.1:8000/.
You can use the /apiTest/ page to test api.
You must log in then test api.