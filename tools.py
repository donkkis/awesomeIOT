from datetime import datetime as dt
import datetime
import time
import math

class Tools(object):
    def parse_unix_ts(self, timestamp):
        return dt.fromtimestamp(math.trunc(timestamp/1000000))
    
    def get_timecluster_dense(self, timestamp):
        return timestamp - datetime.timedelta(seconds = timestamp.second % 30)

    def get_timecluster_rough(self, timestamp):
        timestamp -= datetime.timedelta(minutes = timestamp.minute % 30,
                                              seconds = timestamp.second % 60)
        return timestamp.strftime("%X")
    
    def get_weekday(self, timestamp):
        return timestamp.strftime("%A")

    def date_to_unix(self, date_string):
        return time.mktime(dt.strptime(date_string, '%d.%m.%Y %H:%M:%S.%f').timetuple())

    def get_dnodeid_by_asset_and_name(self, mapping_dict, asset, name):
        return mapping_dict[(asset, name)]

    def get_dnode_shortname(self, name, sn_dict):
        name = name.lower()
        if name in sn_dict:
            return sn_dict[name] 
        return [name[0:7].replace(" ", ""), "null"]
