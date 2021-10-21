#! /bin/bash
url="http://localhost:80/sample"
sampletime=$(date +"%Y-%m-%d %H:%M:%S")
name="wvwgnmwnvw"
latitude="0.0"
longitude="0.0"
temperature="250"
humidity="500"
status="0"
message=""
post="rtype=sample&sampletime=$sampletime&name=$name&latitude=$latitude&longitude=$longitude&temperature=$temperature&humidity=$humidity&status=$status&message=$message"
wget --quiet --server-response --timeout=5 --post-data="$post" $url -O-
