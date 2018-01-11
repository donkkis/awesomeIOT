import requests
import getpass
import csv
from datetime import datetime as dt
import time

class Wrmclient(object):
    """
        config = {
                'username' : WRM API username,
                'password' : WRM API password,
                'mapping_file' : path csv file containing device mappings,
                'shortname_dict' : dictionary, long datanode names to short ones ,
                'asset_dict' : nothing at the moment,
                'base_url' : WRM api server, eg. https://my.iot-ticket.com/rest/v1,
                }
                
        mapping_dict: Dictionary (string, string) -> string containing mapping
        assetID and datanode name to datanode ID
        s: a requests.session instance
    """

    def __init__(self, config):
        #build the mapping (asset, name) --> datanodeID
        self.mapping_dict = {}
        self.asset_dict = config['asset_dict']
        self.shortname_dict = config['shortname_dict']
        with open(config["mapping_file"], 'r') as c:
            reader = csv.reader(c, delimiter=',')
            for row in reader:
                self.mapping_dict[(row[0], row[2])] = row[1]

        #Initialize session and test
        self.s = requests.Session()
        #user = input('User: ')
        #pw = getpass.getpass()
        self.user = config['username']
        self.pw = config['password']
        self.base_url = config['base_url']
        r = self.s.get(self.base_url, auth=(self.user, self.pw))
        print("Response from server: ", r.status_code)

    def parse_unix_ts(self, timestamp):
        return dt.fromtimestamp(timestamp/1000000)

    def date_to_unix(self, date_string):
        return time.mktime(dt.strptime(date_string, '%d.%m.%Y %H:%M:%S.%f').timetuple())

    def get_dnodeid_by_asset_and_name(self, asset, name):
        return self.mapping_dict[(asset, name)]

    def get_dnode_shortname(self, name, sn_dict):
        name = name.lower()
        if name in sn_dict:
            return sn_dict[name] 
        return [name[0:5].replace(" ", ""), "null"]

    def write_response_to_csv(self, data, location, name):
        #build output filename from first and last datapoint timestamp and datanode shortname
        first = self.parse_unix_ts(data[0]['ts']).strftime('%d%m%y')
        last = self.parse_unix_ts(data[-1]['ts']).strftime('%d%m%y')
        shortname = self.get_dnode_shortname(name, self.shortname_dict)[0]
        unit = self.get_dnode_shortname(name, self.shortname_dict)[1]

        filename = "output/"+shortname+"_"+first+"_"+last+".csv"
                                
        with open(filename, 'w') as out:
            print('Location,Name,Value,Unit,Timestamp')
            print('Location,Name,Value,Unit,Timestamp', file=out)
            for entry in data:
                date = self.parse_unix_ts(entry['ts']).strftime('%d.%m.%Y %H:%M:%S.%f')
                value = entry['v']
                print(location, name, value, unit, date, sep=',')
                print(location, name, value, unit, date, sep=',', file=out)
        print("Output saved to", filename)

    def request_data(self, location, name, start, stop):
        dnodeid = self.get_dnodeid_by_asset_and_name(location, name)

        begin_epoch = self.date_to_unix(start)
        end_epoch = self.date_to_unix(stop)
        begin = int(begin_epoch*1000000)
        end = int(end_epoch*1000000)

        payload = {'begin' : begin, 'end' : end}
        r = self.s.get(self.base_url+'/datanodes/'+dnodeid+'/processdata', params=payload)
        data = r.json()["items"]
        return location, name, data
