import json
import wrmclient
import wrmdbclient
import click
import getpass
from datetime import datetime as dt

def init_config(conf_data):
    return {
        'username' : conf_data["username"],
        'password' : conf_data["password"],
        'mapping_file' : conf_data["mapping_file"],
        'shortname_dict' : conf_data["shortname_dict"],
        'asset_dict' : conf_data["asset_dict"],
        'base_url' : conf_data["base_url"],
        'db_url' : conf_data["db_url"],
        'db_schema' : conf_data["db_schema"],
        'db_user' : conf_data["db_user"],
        'db_pw' : conf_data["db_pw"],
        'db_path' : conf_data["db_path"] #unused
        }


@click.command()
@click.option('--c', default="res/config.json", help="Path to config file (Default = res/config.json)")
@click.option('--l', help="Location/asset ID (Required)")
@click.option('--n', help="Cleartext datanode name (Required)")
@click.option('--begin', help="Begin time in dd.mm.yyyy hh:mm:ss.ssssss")
@click.option('--end', help="End time in dd.mm.yyyy hh:mm:ss.ssssss")
@click.option('--o', default=True, help="Write output to csv file (Default = True)")
@click.option('--s', default=False, help="Silent mode (Not implemented yet)")
def run(l, n, o, s, c, begin, end):

    conf_data = json.load(open(c))
    config = init_config(conf_data)

    if not config["username"] or not config["password"]:
        config["username"] = input("Username: ")
        config["password"] = getpass.getpass("Password: ")
    
    tic = dt.now()
    client = wrmclient.Wrmclient(config)
    dbclient = wrmdbclient.WrmDbClient(config)
    location, name, data = client.request_data(l, n, begin, end)
    toc = dt.now()
    print("Query submitted in", toc-tic, ", returned", len(data), "records")
    tic = dt.now()
    if o:
        #client.write_response_to_csv(data, l, n)
        dbclient.commit_results_to_db(data, l, n)
    toc = dt.now()
    print("Database write operation took", toc - tic)

if  __name__ == '__main__':
    run()
