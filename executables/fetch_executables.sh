#!/bin/bash

pftp -vin hgdownload.cse.ucsc.edu <<EOC
user "anonymous" ""
lcd $PWD
cd /apache/htdocs/admin/exe/linux.x86_64/
mget *
EOC
