#!/bin/bash

cd $(pwd)/lib
sudo php run.php --verbose --target=/dev/nvme0n1 --test=iops --test=latency --test=throughput --spec=enterprise --threads_per_core_max=1 --nvmeformat
