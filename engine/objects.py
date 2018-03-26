
import numpy as np
from numpy import array as ar
from copy import copy

class GameObj(object):
    def __init__(s, **kwargs):
        s.__dict__.update(kwargs)

    def w(s, **kwargs):
        res = copy(s)
        res.__dict__.update(kwargs)
        return res

    def speed(s):
        try: return s._speed
        except AttributeError:
            s._speed = np.sqrt(s.d.dot(s.d))
            return s._speed

    def __str__(s): return repr(s)

    def __repr__(s):
        return "GameObj(%s)" % \
            ', '.join('%s=%r' % (k, v) for k, v in s.__dict__.items())

def new_object(pos=(0.,0.), d=(0.,0.), radius=1., time=0., weight=1.):
    return GameObj(pos=ar(pos), d=ar(d),
            radius=radius, time=time, weight=weight)

def no_collision_update(gobj, dtime):
    return gobj.w(pos=(gobj.pos + gobj.d * dtime), time=(gobj.time + dtime))

def may_collide(go1, go2, dtime):
    dpos = go1.pos - go2.pos
    reach = go1.radius + go2.radius + (go1.speed() + go2.speed()) * dtime
    return dpos.dot(dpos) < reach*reach

def will_collide(go1, go2, dtime): return "STUB"

