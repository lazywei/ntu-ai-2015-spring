# Animation

Using redis to save our maps

1. pip install redis
2. redis-server

```
from animation.interactive import *

# init
r = RedisQueue('key')
r.put([map, map2])
dr_ = Drawer(r)

# get map

r.put([map_3, map_4])
r.put([map_5])

```
