************************************************************************
file with basedata            : cm242_.bas
initial value random generator: 1683414677
************************************************************************
projects                      :  1
jobs (incl. supersource/sink ):  18
horizon                       :  137
RESOURCES
  - renewable                 :  2   R
  - nonrenewable              :  2   N
  - doubly constrained        :  0   D
************************************************************************
PROJECT INFORMATION:
pronr.  #jobs rel.date duedate tardcost  MPM-Time
    1     16      0       31        6       31
************************************************************************
PRECEDENCE RELATIONS:
jobnr.    #modes  #successors   successors
   1        1          3           2   3   4
   2        2          1           5
   3        2          3           8   9  11
   4        2          2           6  10
   5        2          3           7  11  13
   6        2          2          12  13
   7        2          3           8   9  12
   8        2          2          10  14
   9        2          2          10  14
  10        2          2          15  17
  11        2          1          17
  12        2          1          14
  13        2          2          15  16
  14        2          3          15  16  17
  15        2          1          18
  16        2          1          18
  17        2          1          18
  18        1          0        
************************************************************************
REQUESTS/DURATIONS:
jobnr. mode duration  R 1  R 2  N 1  N 2
------------------------------------------------------------------------
  1      1     0       0    0    0    0
  2      1     1       1    0   10    8
         2     7       0    8    8    8
  3      1     3       0    6    6    9
         2    10       2    0    4    7
  4      1     1       0    5    4    8
         2     3       0    4    3    5
  5      1     7       1    0    6    5
         2     7       0    9    7    5
  6      1     7       0   10    1    9
         2     9       0    9    1    4
  7      1     3      10    0    6    8
         2    10       0    6    6    8
  8      1     9       0    5    6    2
         2    10       9    0    4    2
  9      1     1       5    0    3    8
         2    10       0    6    2    7
 10      1     6       7    0    7   10
         2     8       0    4    6    6
 11      1     8       6    0    6    4
         2    10       6    0    5    3
 12      1     3       0    6    6    6
         2     9       6    0    6    5
 13      1     8       0    3    8    9
         2     9       3    0    6    9
 14      1     1       8    0    7    8
         2     7       8    0    6    4
 15      1     1       5    0    7    6
         2    10       5    0    6    6
 16      1     5       0    3    5    6
         2    10       7    0    4    3
 17      1     5       0    9    4    5
         2     8       0    7    3    5
 18      1     0       0    0    0    0
************************************************************************
RESOURCEAVAILABILITIES:
  R 1  R 2  N 1  N 2
   19   17   85   99
************************************************************************
