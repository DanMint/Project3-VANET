# Project3-VANET

## How to run above code

1. Go to your ns folder (for me its cd ./ns-3.39)
2. cd ./scratch
3. vim one-base-station.cc
4. paste in the code
5. cd ../
6. ./ns3 build
7. ./ns3 run one-base-station

## The output
========================================
    VANET V2I Simulation Configuration
========================================
Vehicles: 10
Base Station IP: 10.1.1.11
TX Power: 23 dBm
Data Rate: 2048kb/s
Packet Size: 1024 bytes
Packet Interval: 0.1 seconds
Simulation Time: 60 seconds
----------------------------------------

Vehicle IP Addresses:
  Vehicle 0: 10.1.1.1
  Vehicle 1: 10.1.1.2
  Vehicle 2: 10.1.1.3
  Vehicle 3: 10.1.1.4
  Vehicle 4: 10.1.1.5
  Vehicle 5: 10.1.1.6
  Vehicle 6: 10.1.1.7
  Vehicle 7: 10.1.1.8
  Vehicle 8: 10.1.1.9
  Vehicle 9: 10.1.1.10
========================================


Starting V2I simulation...
Vehicles sending data to base station...
Simulation Progress: 10/60 seconds
Max Packets per trace file exceeded
Simulation Progress: 20/60 seconds
Simulation Progress: 30/60 seconds
Simulation Progress: 40/60 seconds
Simulation Progress: 50/60 seconds

========================================
         SIMULATION RESULTS
========================================

--- BASE STATION STATISTICS ---
Total Data Received: 18230 KB
Total Data Received: 17.8027 MB
Average Throughput: 2.489 Mbps

--- PER-VEHICLE STATISTICS ---

Vehicle 0 (10.1.1.1):
  TX Packets: 14749
  RX Packets: 0
  TX Bytes: 15515948
  RX Bytes: 0
  Delivery Ratio: 0%
  Throughput: 0 kbps

Vehicle 1 (10.1.1.2):
  TX Packets: 14724
  RX Packets: 6516
  TX Bytes: 15489648
  RX Bytes: 6854832
  Delivery Ratio: 44.2543%
  Avg Delay: 446 ms
  Throughput: 913.978 kbps

Vehicle 2 (10.1.1.3):
  TX Packets: 14699
  RX Packets: 2196
  TX Bytes: 15463348
  RX Bytes: 2310192
  Delivery Ratio: 14.9398%
  Avg Delay: 479 ms
  Throughput: 308.026 kbps

Vehicle 3 (10.1.1.4):
  TX Packets: 14674
  RX Packets: 5407
  TX Bytes: 15437048
  RX Bytes: 5688164
  Delivery Ratio: 36.8475%
  Avg Delay: 487 ms
  Throughput: 758.422 kbps

Vehicle 4 (10.1.1.5):
  TX Packets: 14649
  RX Packets: 1969
  TX Bytes: 15410748
  RX Bytes: 2071388
  Delivery Ratio: 13.4412%
  Avg Delay: 466 ms
  Throughput: 276.185 kbps

Vehicle 5 (10.1.1.6):
  TX Packets: 14624
  RX Packets: 868
  TX Bytes: 15384448
  RX Bytes: 913136
  Delivery Ratio: 5.93545%
  Avg Delay: 433 ms
  Throughput: 121.751 kbps

Vehicle 6 (10.1.1.7):
  TX Packets: 14599
  RX Packets: 931
  TX Bytes: 15358148
  RX Bytes: 979412
  Delivery Ratio: 6.37715%
  Avg Delay: 473 ms
  Throughput: 130.588 kbps

Vehicle 7 (10.1.1.8):
  TX Packets: 14574
  RX Packets: 334
  TX Bytes: 15331848
  RX Bytes: 351368
  Delivery Ratio: 2.29175%
  Avg Delay: 467 ms
  Throughput: 46.8491 kbps

Vehicle 8 (10.1.1.9):
  TX Packets: 14549
  RX Packets: 9
  TX Bytes: 15305548
  RX Bytes: 9468
  Delivery Ratio: 0.0618599%
  Avg Delay: 499 ms
  Throughput: 1.2624 kbps

Vehicle 9 (10.1.1.10):
  TX Packets: 14524
  RX Packets: 0
  TX Bytes: 15279248
  RX Bytes: 0
  Delivery Ratio: 0%
  Throughput: 0 kbps

--- OVERALL STATISTICS ---
Total TX Packets (all vehicles): 146365
Total RX Packets (at base station): 18230
Overall Packet Delivery Ratio: 12.4552%
Average End-to-End Delay: 465.942 ms

========================================
    Simulation Completed Successfully!
========================================

## High level overview:
Position  | Diagram | Actual Result | Match?
----------|---------|---------------|--------
V0 (0m)   |   ❌    |     0%        |   ✅
V1 (100m) |   44%   |   44.25%      |   ✅
V2 (200m) |   15%   |   14.94%      |   ✅
V3 (300m) |   37%   |   36.85%      |   ✅
V4 (400m) |   13%   |   13.44%      |   ✅
V5 (500m) |   6%    |   5.94%       |   ✅
V6 (600m) |   6%    |   6.38%       |   ✅
V7 (700m) |   2%    |   2.29%       |   ✅
V8 (800m) |   0%    |   0.06%       |   ✅
V9 (900m) |   ❌    |     0%        |   ✅

                        BASE STATION @ 500m
                                📡
                                |
                Coverage sweet spot (≈300-400m radius)
            <---------------------|--------------------->
    
    0m    100m   200m   300m   400m   500m   600m   700m   800m   900m
    V0     V1     V2     V3     V4    V5     V6     V7     V8     V9
    🚗     🚗     🚗     🚗     🚗    🚗     🚗     🚗     🚗     🚗
    
  