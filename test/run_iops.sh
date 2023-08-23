#!/bin/bash

DEV_UNDER_TEST="/dev/sda"
#SPEC="client"
SPEC="enterprise"

echo "Device '$DEV_UNDER_TEST' must be secure erased manually! See https://grok.lsu.edu/article.aspx?articleid=16716"
read -p "Press [Enter] to confirm this has been done, or Ctrl-C to exit"

cd $(pwd)/lib
sudo php run.php --verbose --target=$DEV_UNDER_TEST --test=iops --spec=$SPEC --no-secureerase --notrim --nozerofill

# End of script
