import os
import sys
import time

from cassandra.cluster import Cluster
cassandra_hosts = os.environ.get('CASSANDRA_HOSTS', 'localhost')

for r in range(1, 5):
    try:
        print("Connecting %i" % r)
        cluster = Cluster(cassandra_hosts.split(','))
        session = cluster.connect()
        print("Connected")
        session.shutdown()
        sys.exit(0)
    except Exception as exc:
        print(exc)
        print("Wait 10 seconds")
        time.sleep(10.0)
sys.exit(1)
