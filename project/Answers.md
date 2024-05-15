Task 4:
1. The issue is that the query that is submitted by the code is not parameterised and, when the test submits 
its query it ends it early and appends drop table to the end which would result in the entire database being lost
not parametising queries within the code can lead to issues such as data exposure and loss, corrupted databases and
integrity and could also be used to gain access to the database which allows the data to be stolen, controlled or manipulated.
This violates the SQL Injection security principle as well as unauthorised access.
2. Implemented
3. The updated code parametises the query to avoid sql injection as the user input is treated as data dn not a query
4. The updated SQL test checks that the database exists and that it is not corrupted to properly check for injection flaws

Task 5
1. implemented
2. Works
3. Plan
   1. Initially perform a database backup and create a testing grounds for the changes to ensure they work
   2. Test the background script to hash works by inserting a plaintext password and hashing it with the script and ensure user can still login
and system correctly checks hashed password
   3. Plan downtime and verify how long it will take to deploy and convert plaintext to hashed
   4. First update the auth code to ensure it can handle hashed passwords as well and unhashed while passwords are hashed in the background
   5. Monitor live system and database actively to see how many passwords are hashed
This follows the CIA principles by protecting confidentiality through a safe and secure hash, integrity by ensuring all
the hashes maintain the same plaintext data and the database is not corrupted and follows availability as the deployment has
a backup in case of an issue to maintain uptime and to ensure continuous access

Task 6
1. the website is vulnerable to Stored attack as the name is stored in the database then displayed onto the page
you could inject a js script tag such as \<script>alert('XSS');</script> which when the user logs in should create an alert ont he page
that says "XSS", unfortunately this attack doesn't work as the {{ name }} that is used to render the variable
auto sanitises the variable due to flasks templating engine jinja2
2. Implemented