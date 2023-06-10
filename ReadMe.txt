# Kasheesh interview Erik R


## Project Description

Interview assessment for Erik R.
The program is based on a flask RESTapi and a python/sqlite3 backend (justifications for packages below).
There are two endpoints: allByUser, netMerchant that handle the calls described in the assignment (more on them below).
There is also a folder "Tests" containing unit tests for my different files.

## Installation

1. Clone the repository:
   ```shell
   git clone https://github.com/erikreimert/kasheesh.git

2. Most of the project is based on stock python, please download python 3.9^. I'll list out the dependencies it has in case some of them are not stock:

- flask (need to install separately)
- unittest
- pandas (need to install separately)
- sqlite3

If you have to install any of these they should be available through pip (pip install [name of dependency])

3. To run the project you have to run the main.py file. Open a command line, find the directory with the project and run
"python main.py".

4. The project goes by default to this URL http://127.0.0.1:5000. You can interact with the two endpoints at
    http://127.0.0.1:5000/allByUser
    http://127.0.0.1:5000/netMerchant

    I recommend using Postman for this, it's easy to set up and use. By the way, make sure that the headers include
    Content-Type: application/json
    Below is a sample payload for each endpoint correspondingly

    {
    "user_id": 38493
    }
    {
    "merchant_type_code": 5200
    }

5. I included the pythonsqlite.db file already in the folder, but if you are interested in seeing how its created
   you can check it out on the dbManager.py file. also, I commented out the line that inits that on the main since its
   already created, but feel free to delete the file and recreate it (by uncommenting that line) on a run.

6. Unit tests are included on the /tests folder in case you need to sanity check anything.


## Justifications

Database

    I went with SqLite because it's a lightweight and easy to implement db that had everything I needed for this
    situation (It being easy to implement meant I could do the assignment comfortably by the due date, and sometimes,
    being first to the market does count). The two big drawbacks I saw for this database are the fact that there's
    no right outer join and for each. However, I did not need these features to complete the assignment.
    NOTE: In a real world situation I would go for something more akin to postGreSQL given its more robust and scalable.

Flask v Django

    In the past I have chosen Django given how much more scalable and robust it can be. However, in the past Django
    has proven to be difficult and time-consuming at times. Given the short timeframe I had, and the very simple
    nature of the task Flask would more than cover my bases, thus I chose it (also I had never used flask before and this
    was a golden learning opportunity). Also, Flask is RESTful which was something you guys were looking for, so thats
    a plus. Also, developing the endpoints and API for it was a breeze, so I'm happy I chose it.
    NOTE: The scalability of DJango makes it attractive for real projects, specially given the lack of security I found
    flask to have (didn't require auth keys or anything to do my API calls on it).
