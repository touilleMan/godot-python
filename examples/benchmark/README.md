Test machine AMD Ryzen 7 PRO 6850U (integrated GPU) with 16Go RAM:

Test                              | Nodes  | Avg FPS | Min FPS | Max FPS
----------------------------------|--------|---------|---------|--------
**100 nodes**                     |        |         |         |
Python builtins                   |  100   | 117.4   |  57.0   | 145.0
GDScript builtins                 |  100   | 144.9   | 144.0   | 145.0  x1.23 faster
Python Godot classes              |  100   | 138.9   | 138.0   | 141.0
GDScript Godot classes            |  100   | 144.0   | 138.0   | 145.0  x1.04 faster
Python calls Python class         |  100   | 144.7   | 144.0   | 145.0
GDScript calls Python class       |  100   | 145.0   | 145.0   | 145.0  x1.00 faster
**1000 nodes**                    |        |         |         |
Python builtins                   | 1000   | 116.2   |  58.0   | 145.0
GDScript builtins                 | 1000   | 144.2   | 143.0   | 145.0  x1.24 faster
Python Godot classes              | 1000   |  35.0   |  13.0   |  82.0
GDScript Godot classes            | 1000   | 119.3   |  13.0   | 145.0  x3.41 faster
Python calls Python class         | 1000   | 141.0   | 132.0   | 145.0
GDScript calls Python class       | 1000   | 143.1   | 140.0   | 145.0  x1.01 faster
**10000 nodes**                   |        |         |         |
Python builtins                   | 10000  |  16.1   |   1.0   |  21.0
GDScript builtins                 | 10000  |  34.3   |  13.0   |  42.0  x2.13 faster
Python Godot classes              | 10000  |   1.3   |   1.0   |   2.0
GDScript Godot classes            | 10000  |  20.4   |   1.0   |  27.0  x16.21 faster
Python calls Python class         | 10000  |  58.8   |  19.0   |  71.0
GDScript calls Python class       | 10000  |  52.0   |  31.0   |  60.0  x0.88 faster
