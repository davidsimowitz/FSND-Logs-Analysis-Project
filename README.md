Logs Analysis
=================================


Udacity - Full Stack Web Developer Nanodegree
---------------------------------------------
P3: Logs Analysis

This project's goal was to build an internal command line reporting tool that uses information queried from a newspaper site's database to determine what kind of articles the newspaper site's readers prefer. The tool determines the most popular articles, as well as authors, and days where the site experienced a high level of user request errors based on user activity and web server logs.


Requirements
------------

+ [Python 3](https://www.python.org/downloads/) is installed.
+ This can be verified by running the following command in the terminal:
```bash
$ python -V
```
+ [Virtual Box](https://www.virtualbox.org/wiki/Downloads) is installed.
+ [Vagrant](https://www.vagrantup.com/downloads.html) is installed.
+ [VM configuration files](https://github.com/udacity/fullstack-nanodegree-vm) are setup.
+ [Git](https://git-scm.com/downloads) is installed.
  (Optional, if you wish to clone the project repository.)


Usage
-----

```bash
$ git clone https://github.com/davidsimowitz/fullstack-nanodegree-project-3.git
```
  + Above command is optional.
  + Alternatively you may download the files into the directory.
```bash
$ cd fullstack-nanodegree-project-3
```
  + Verify the following files are present before continuing:
    * summary_reporting_tool.py
    * newsdata.zip
    * fsnd-virtual-machine.zip
    * SUMMARY_REPORT_2017-07-14_01:09:19_UTC.log  (generated report example)

* Install Virtual Box, then Vagrant. (If not previously installed)
* Unzip the fsnd-virtual-machine.zip file (This contains the VM files).
* Unzip the newsdata.zip file (contains the PostgreSQL database for this project)

* Copy summary_reporting_tool.py and newsdata.sql to the vagrant directory in the VM.
```bash
$ cp summary_reporting_tool.py ./FSND-Virtual-Machine/vagrant/summary_reporting_tool.py
$ cp newsdata.sql ./FSND-Virtual-Machine/vagrant/newsdata.sql
```
* Enter the VM directory.
```bash
$ cd FSND-Virtual-Machine/vagrant/
```
* Startup the VM. (This may take a while)
```bash
$ vagrant up
```
* Log in to the VM.
```bash
$ vagrant ssh
```
* Enter the shared vagrant directory and load the data from newsdata.sql.
```bash
$ cd /vagrant
$ psql -d news -f newsdata.sql
```
* Run the summary_reporting_tool.py report generator from the command-line. The results will automatically be output to the terminal once the command is run. A log file will also be generated in the current directory.
```bash
$ ./summary_reporting_tool.py
```


Output
------

* The summary tool runs from the command line and does not take any input from the user. Instead it connects to the database, uses SQL queries to analyze the log data, and finds the following:
  + Most popular three articles of all time, sorted by popularity (most to least).
  + Most popular article authors of all time, sorted by popularity (most to least).
  + Days where more than 1% of user requests led to errors.
