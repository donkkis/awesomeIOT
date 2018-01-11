# awesomeIOT
Simple command line tool for interfacing IOT Ticket's WRM API

Needs datanode_mapping.csv project-specific file in /res, which should be csv in format: assetID,DatanodeID,DatanodeName. 

Basic use example:

$ wrmapplication.py --l=186973 --n="Temp Ambient" --begin="10.01.2018 06:00:00.000000" --end="10.01.2018 12:00:00.000000"

For complete list of currently supported option, try:

$ wrmapplication.py --help

Username/password promting can be overridden for dev/testing purposes by editing config.json, otherwise it's not recommended
