from peewee import *
import tools
import entry

class WrmDbClient(object):

    def __init__(self, config):
        self.shortname_dict = config['shortname_dict']
        self.tools = tools.Tools()
        self.db = SqliteDatabase('ebus_turku.db')

    def commit_results_to_db(self, data, loc, name):
        self.db.connect()
        self.db.create_tables([entry.Entry])
        un = self.tools.get_dnode_shortname(name, self.shortname_dict)[1]
        
        new_entry = []
        #Build entry ORM objects from  query data
        for row in data:
            ts = self.tools.parse_unix_ts(row['ts'])
            dense_cluster = self.tools.get_timecluster_dense(ts)
            rough_cluster = self.tools.get_timecluster_rough(ts)
            weekday = self.tools.get_weekday(ts)
            v = row['v']
            new_entry.append({'timestamp' : ts, 
                              'timecluster_dense' : dense_cluster,
                              'timecluster_rough' : rough_cluster,
                              'weekday' : weekday,
                              'value' : v, 
                              'datanode' : name, 
                              'location' : loc, 
                              'unit' : un})
        
        #Batch insert into db
        #http://docs.peewee-orm.com/en/latest/peewee/querying.html#bulk-inserts
        with self.db.atomic():
            for idx in range(0, len(new_entry), 100):
                entry.Entry.insert_many(new_entry[idx:idx+100]).execute()

        self.db.close()