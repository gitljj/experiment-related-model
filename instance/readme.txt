The output text file contains the following information:

instance type
  1. number of part, number of alternative build orientation for each part, and number of part type

machine parameters
  1. build platform dimensions (length, width, height)
  2. power of different subsystems
  3. power coefficient of different subsystems (11 rows by 7 columns)
11 rows for subsystems: 1. bs - basic subsystems 2. ht - platform heater 3. wc - water cooling unit 4. co - water circulation unit 5. lsb - laser-scanning border  6. lfc - laser-filling contour 7. lvh - laser-volume hatching 8. lss - laser-supports building 9. rm - recoater motor 10. ev - electric valves 11. gp - gas circulation pump Motor
7 columns for subprocesses: 1.ph - preheating 2.sb - scanning border 3.fc - filling contour 4.vh - volume hatching 5.ss - supports suilding 6.rc - recoating 7.co - Cooling

process parameters 
  1.minimum distance of parts,minimum distance between part and platform boundary, number of lasers, hatching distance, laser scanning speed, layer thickness, preheating time, cooling time)

part information
  1. type of part, number of this part type, part volume, part surface area
  2. projection dimensions (length, width, height) and support structure for each part in different build orientation

The data format is like this:

///////////////////////////////////////////

num_parts num_orientation type_parts

L W H
power of subsystems
power coefficient array 

min_distance_parts min_distance_part_platform num_laser hatch_distance_volume hatch_distance_support laser_speed_ border laser_speed_contour laser_speed_volume laser_speed_support layer_thickness heat_time cool_time

part_type num_part volume surface_area
 l w h support#orientation_1
 l w h support#orientation_2

part_type num_part volume surface_area
 l w h support#orientation_1
 l w h support#orientation_2

Suppose we have an instance below :

////////////////////////////////////////

6 2 2

268 268 315 
569.7 1122.3 713.3 1739.4 1770.92 1770.92 2022.92 2022.92 52.1 32.1 69.1 
1 1 1 1 1 1 1
1 0.4826 0.4826 0.4826 0.4826 0.4826 0
1 1 1 1 1 1 1
0.168 0.353 0.353 0.353 0.353 0.353 0.216
0 1 0 0 0 0 0
0 0 1 0 0 0 0
0 0 0 1 0 0 0
0 0 0 0 1 0 0
0 0 0 0 0 1 0
1 1 1 1 1 1 0
0 1 1 1 1 1 0

10 10 2 0.13 0.18 730 1650 1650 1000 0.03 2115 5380 

1 3 6744.0 8607.8
57.539 24.618 18.0 1724
38.839 24.539 41.670 2596

2 3 37635.0 17532.0
73.0 64.0 51.93 26353
78.349 72.716 76.410 14668

/////////////////////////////////////////////

The illustration is as below:

num_parts=6 num_orientaion=2 type_parts=2

L=268 W=268 H=315
power_of_bs=569.7 power_of_ht=1122.3 power_of_wc=713.3 power_of_co=1739.4 power_of_lsb=1770.92 power_of_lfc=1770.92 power_of_lvh=2022.92 power_of_lss=2022.92 power_of_rm=52.1 power_of_ev=32.1 power_of_gp=69.1
        | ph    | sb    | fc    | vh    | ss    | rc    | co    |
--------------------------------------------------------------
bs    | 1     | 1     | 1     | 1     | 1     | 1     | 1     |
--------------------------------------------------------------
ht    | 1     | 0.4826| 0.4826| 0.4826| 0.4826| 0.4826| 0     |
--------------------------------------------------------------
wc    | 1     | 1     | 1     | 1     | 1     | 1     | 1     |
--------------------------------------------------------------
co    | 0.168 | 0.353 | 0.353 | 0.353 | 0.353 | 0.353 | 0.216 |
--------------------------------------------------------------
lsb   | 0     | 1     | 0     | 0     | 0     | 0     | 0     |
--------------------------------------------------------------
lfc   | 0     | 0     | 1     | 0     | 0     | 0     | 0     |
--------------------------------------------------------------
lvh   | 0     | 0     | 0     | 1     | 0     | 0     | 0     |
--------------------------------------------------------------
lss   | 0     | 0     | 0     | 0     | 1     | 0     | 0     |
--------------------------------------------------------------
rm    | 0     | 0     | 0     | 0     | 0     | 1     | 0     |
--------------------------------------------------------------
ev    | 1     | 1     | 1     | 1     | 1     | 1     | 0     |
--------------------------------------------------------------
gp    | 0     | 1     | 1     | 1     | 1     | 1     | 0     |
--------------------------------------------------------------

min_distance_parts=10 min_distance_part_platform=10 num_laser=2 hatch_distance_volume=0.13 hatch_distance_support=0.18 laser_speed_border=730 laser_speed_contour=1650 laser_speed_volume=1650 laser_speed_support=1000 layer_thickness=0.03 preheat_time=2115 cool_time=5380

part_type=1 num_part=3 volume=6744.0 suface_area=8607.8
l=57.539 w=24.618 h=18.0 support=1724 # orientation_1
l=38.389 w=24.539 h=41.670 support=2596 # orientation_2

part_type=2 num_part=3 volume=37635.0 surface_area=17532.0
l=73.0 w=64.0 h=51.93 support=26353 # orientation_1
l=78.349 w=72.716 h=76.410 support=14668 # orientation_2
