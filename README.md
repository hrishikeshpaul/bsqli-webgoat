# Blind SQL Injection: WebGoat
This project demonstrates a very common cyber attack called blind SQL injection. By analyzing specific fields that are vulnerable to SQL injection, we have used the WebGoat servers as the victim to test the concept of blind SQL injection. The paper discusses the ways in which the servers were attacked, the data that was retrieved, the method that was followed in order to achieve that, and then concludes with a few practices that can potentially prevent such attacks.

### Code Execution

**Requirements**
- Python3
- WebGoat

Please make sure you have WebGoat up and running of the code to execute perfectly. If you do not have WebGoat, you can still run the code, but can only view the results (present in the outputs folder) and not won't be able to run any queries. The following steps demonstrate how the code can be downloaded and executed,
```shell script
$ git clone https://github.com/hrishikeshpaul/bsqli-webgoat.git
$ cd bsqli-webgoat
$ python3 main.py
```

**Note:** Please make sure to update the `cookie` in the `main()` function. This can be done by 
typing `document.cookie()` in the web inspector having logged into WebGoat.

**Python Libraries**

Below are a list of python libraries that were used and how you can get them,

1. pickle (for object serialization): `pip install pickle`
2. tabulate (for printing beautification): `pip install tabulate`


For an detailed explanation of the working of the code, please see the [report](https://github.com/hrishikeshpaul/bsqli-webgoat/blob/master/assets/CDC_Assignment_1.pdf).