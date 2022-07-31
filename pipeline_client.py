import os
import httpx
import datetime
import hashlib
import argparse
e = {}

base_url = "http://127.0.0.1:5000"

# skip variables that match any part of these
skip_list = ["PATH", "SECRET", "PASS", "VAULT"]

for k in os.environ:
    include = True
    for s in skip_list:
        if s in k:
            include = False
    if include:
        e[k] = os.environ.get(k)
# this is already a diction value, so it's good to go

# extract what you may want, such as project

e['project'] = "test-project"
# TODO this will be something else that makes the run unique and derivable from the attributes
e['timestamp'] = datetime.datetime.now().strftime("%s")

hash_string = e['project'] + e['timestamp']  # from timestamp
hash_value = hashlib.md5(hash_string.encode('utf-8')).hexdigest()
h = {}
# TODO hard code for now until we can figure out the cache
hash_value = "ffa4b3585dd87bc72b6c2fb74588e8ad"
h["hash_value"] = hash_value
h["state"] = "WORKING"


def insert():
    # fire and forget
    try:
        r: httpx.post(url=base_url + "/insert_pipeline", json={'attributes': e})
    finally:
        print(r)


def update(status):
    try:
        r = httpx.post(url=base_url + "/update_state", json=h)
    finally:
        print(r)


parser = argparse.ArgumentParser(description='Take Action')
parser.add_argument('action', type=str, default="insert",
                    help='take action, either insert or update')

if __name__ == "__main__":
    """ update or insert """
    args = parser.parse_args()
    if args.action == "insert":
        insert()
    if args.action == "update":
        update() # this needs to capture some fail status from attributes or otherwise


