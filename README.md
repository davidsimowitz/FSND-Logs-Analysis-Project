FSND - Logs Analysis Project
=================================

Udacity - Full Stack Web Developer Nanodegree
---------------------------------------------
Logs Analysis Project

Build an internal reporting tool that will use information from a newspaper site's database to discover what kind of articles the newspaper site's readers like.

The news database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, the summary tool will answer questions about the site's user activity.

The summary tool runs from the command line and does not take any input from the user. Instead it connects to the database, uses SQL queries to analyze the log data, and finds the following:
 + Most popular three articles of all time, sorted by popularity (most to least).
 + Most popular article authors of all time, sorted by popularity (most to least).
 + Days where more than 1% of user requests lead to errors.

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
$ git clone https://github.com/davidsimowitz/FSND-Logs-Analysis-Project.git
```
  + Above command is optional.
  + Alternatively you may download the files into the directory.
```bash
$ cd FSND-Logs-Analysis-Project
```
  + Verify the following files are present before continuing:
    * summary_reporting_tool.py
    * newsdata.zip
    * fsnd-virtual-machine.zip
    * SUMMARY_REPORT_2017-07-14_00:37:26_UTC.log (generated report example)

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
* Enter the shared vagrant directory.
```bash
$ cd /vagrant
$ ls
```
* Load the data from newsdata.sql
```bash
$ psql -d news -f newsdata.sql
```
* Run the summary_reporting_tool.py report generator from the command-line.
```bash
$ ./summary_reporting_tool.py
```
  + The results will automatically be output to the terminal once the command is run. A log file will also be generated in the current directory.
