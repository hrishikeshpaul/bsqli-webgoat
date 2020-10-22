# Blind SQL Injection: WebGoat
This paper demonstrates a very common cyber attack called blind SQL injection. By analyzing specific fields that are vulnerable to SQL injection, we have used the WebGoat servers as the victim to test the concept of blind SQL injection. The paper discusses the ways in which the servers were attacked, the data that was retrieved, the method that was followed in order to achieve that, and then concludes with a few practices that can potentially prevent such attacks.


## Introduction

The paper demonstrates BSQLi by attacking OWSAP WebGoat's SQL Server. It starts off by explaining some preliminaries that describes the code structure, a few SQL concepts that were used, and how the code can be downloaded and executed. Then the paper moves on to discuss the methodology that was followed in order to successfully attack the WebGoat Servers by explaining each and every attack. The section after that discusses some results that lists various information that was retrieved from the database. Lastly, the paper proposes a few development practices that can help mitigate such attacks and a few high-level outcomes of the work. 


## Preliminaries

### Code Structure
The attacking scripts are written in Python 3.8. The code is made modular to incorporate changes, following this structure, 
- helpers: This folder contains the functions that felicitate the code for the various attacks. These scripts are the code logic of the project.
- outputs: This folder contains pickle files of the results of the the attacks. One will need to use pickle to retrieve the outputs.
- states: This folder contains the execution states of the program while performing an attack. Since most of the attacks take a considerable amount of time, it was a good idea to save the most recent state of the attack in the event of an error.
- main.py: This is the main script that contains the interface to select the options
- res.py: This script contains resources like the URL.

### SQL Queries

The project uses basic SQL queries to attack the servers. It uses the keyword _EXISTS_ to check if the value of the query is true or false. This is particularly helpful as we want to know whether our injected query was valid or invalid to the server, and based on that access the next moves. The keyword _SUBSTRING_ has been widely used across the project. This is used to match words to those in the database. This keywords helps us to build the words that we are looking for by substituting one character at a time (more on this later in the paper).

### Code Execution
Please make sure you have WebGoat up and running of the code to execute perfectly. If you do not have WebGoat, you can still run the code, but can only view the data and not won't be able to run any queries. The following steps demonstrate how the code can be downloaded and executed,
```shell script
$ git clone https://github.com/hrishikeshpaul/bsqli-webgoat.git
$ cd bsqli-webgoat
$ python3 main.py
```

## Methodology

This section gives an in-depth description of the methods used to conduct the attack. The various subsections chronologically talk about the methodology from finding out where to attack from to description of the various scripts used in the attack. The implementation takes a 2 level approach. In the first level, we build possible names (eg table names, column names, usernames) that could be extracted from the database. The way the injection works is that we use ascii letters, digits and symbol to continuously try to brute force the way into finding the data. At every iteration, we add a character the the already found sequence of letters and check if it is a valid input by analyzing the response from the server. In the second level, once we have a set of possible candidate names, we inject it to see if that exists in the table.