# Massping
### A tool for simutaniously checking avalibility of multiple hosts inspired by BIGPHATTOBY/fineping 


![Header IMG](https://raw.githubusercontent.com/AndersBallegaard/Massping/master/doc/img/header.png)

## Getting started
Massping is a fairly easy tool to use but here is some examples of how to use it

### Install
Install can be done with the one liner below
Remmeber to always read scripts before blindly executing them

    curl -sSL https://raw.githubusercontent.com/AndersBallegaard/Massping/master/install.sh | bash

### Examples
Get a help page:
    
    massping -h

Create list of hosts

    massping -cl

Start massping on all host in file example_hosts.csv (provided in repository)

    massping -c example_hosts.csv


Start massping with hosts from command line argument

    massping -s [name],[address] [name],[address]........

