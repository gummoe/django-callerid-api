# django-callerid-api
A simple API for caller id data written in Python with Django.

<h1>To get started:</h1>
<ul>
<li>Follow the very first section of this tutorial to ensure that you have Python installed: https://docs.djangoproject.com/en/1.8/intro/install/</li>
<li>Ensure that you have SQLite installed: http://www.tutorialspoint.com/sqlite/sqlite_installation.htm</li>
<li>Navigate to the app's root and ensure that the source data file is present and called 'interview-callerid-data.csv'</li>
<li>Open up a terminal in the project root and run <b>python manage.py migrate</b>
</ul>

<h1>Using the app:</h1>
<ul>
  <li>Open up a terminal in the project root and run <b>python manage.py runserver</b>. This defaults to port 8000, but you can specify a different port with <b>python manage.py runserver [whatever port number you want]</b>/<li>
  <li>Navigate to <b>/api/load-file</b> to load the data in. Depending on the size of the file, this could take several minutes.</li>
  <li>Navigate to <b>/api/query?number=[number]</b> to GET a contact record</li>
  <li>POST to <b>/api/number</b> with a JSON body in the following structure to create a new record</li>
<ul>
{
"name": "the name",
"number": "the number",
"context": "the context
}

