
import numpy as np
from numpy import array as ar
from math import sqrt
from copy import copy
from itertools import chain

def dist2(vec): return vec.dot(vec)

class GameObj(object):
    def __init__(s, **kwargs):
        s.__dict__.update(kwargs)

    def w(s, **kwargs):
        res = copy(s)
        res.__dict__.update(kwargs)
        return res

    def __str__(s): return repr(s)

    def __repr__(s):
        return "GameObj(%s)" % \
            ', '.join('%s=%r' % (k, v) for k, v in s.__dict__.items())

def new_object(pos=(0.,0.), d=(0.,0.), radius=1., time=0., weight=1.):
    return GameObj(pos=ar(pos), d=ar(d),
            radius=radius, time=time, weight=weight)

def no_collision_update(gobj, dtime):
    return gobj.w(pos=(gobj.pos + gobj.d * dtime), time=(gobj.time + dtime))

def projection_factor(onto_vec, from_vec):
    return onto_vec.dot(from_vec) / dist2(onto_vec)

def collision_time(go1, go2):
    # use reference coordinates where go2 does not move
    ref_movement = go1.d - go2.d
    # is their movement exactly the same?
    if dist2(ref_movement) <= 0.: return []
    # find how long it takes in ref_movement for go1 to be closest to go2
    nearest_time = projection_factor(ref_movement, go2.pos - go1.pos)
    # are they actually getting further from each other?
    if nearest_time < 0.: return []
    # the distance vector from go2 to the closest passing point
    nearest_dist = go1.pos + nearest_time * ref_movement - go2.pos
    # the distance in which go1 and go2 will collide
    collide_dist = go1.radius + go2.radius
    # square of the distance, from nearest point, along go1's movement,
    # where the collision will happen
    dist_sq_diff = collide_dist*collide_dist - dist2(nearest_dist)
    # will collision happen?
    if dist_sq_diff < 0.: return []
    # scale the distance with go1's movement into time
    return [nearest_time - sqrt(dist_sq_diff / dist2(ref_movement))]

def next_collision(gobjs, maxtime):
    return min(chain([(maxtime, None, None)],((dtime, i1, i2)
        for i1 in range(len(gobjs))
        for i2 in range(i1 + 1, len(gobjs))
        for dtime in collision_time(gobjs[i1], gobjs[i2]))))

def update_until_collision(gobjs, maxtime):
    dtime, i1, i2 = next_collision(gobjs, maxtime)
    return [no_collision_update(o, dtime) for o in gobjs]

