import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple
from .body import RigidBody

@dataclass
class CollisionInfo:
    normal: np.ndarray
    penetration: float
    contact_point: np.ndarray
    body_a: RigidBody
    body_b: RigidBody

def circle_vs_circle(a: RigidBody, b: RigidBody) -> Optional[CollisionInfo]:
    """Detect circle-circle collision."""
    ab = b.pos - a.pos
    distance = np.linalg.norm(ab)
    min_dist = a.radius + b.radius
    
    if distance > min_dist:
        return None
    
    normal = ab / distance if distance > 0 else np.array([1.0, 0.0])
    penetration = min_dist - distance
    contact_point = a.pos + normal * a.radius
    
    return CollisionInfo(normal, penetration, contact_point, a, b)

def circle_vs_line(body: RigidBody, p1: np.ndarray, p2: np.ndarray) -> Optional[CollisionInfo]:
    """Detect circle-line collision."""
    line_vec = p2 - p1
    line_len = np.linalg.norm(line_vec)
    line_dir = line_vec / line_len
    to_circle = body.pos - p1
    proj = np.dot(to_circle, line_dir)
    proj = np.clip(proj, 0, line_len)
    closest = p1 + line_dir * proj
    to_closest = body.pos - closest
    dist = np.linalg.norm(to_closest)
    
    if dist > body.radius:
        return None
    
    normal = to_closest / dist if dist > 0 else np.array([0.0, 1.0])
    penetration = body.radius - dist
    contact_point = body.pos - normal * body.radius
    
    return CollisionInfo(normal, penetration, contact_point, body, None)

def resolve_collision(info: CollisionInfo) -> None:
    """Resolve collision using impulse-based response."""
    a, b = info.body_a, info.body_b
    
    if a.is_static:
        if b is not None:
            b.pos += info.normal * info.penetration
        return
    if b is None or (hasattr(b, 'is_static') and b.is_static):
        a.pos -= info.normal * info.penetration
        v = a.vel
        v_n = np.dot(v, info.normal)
        if v_n < 0:
            restitution = a.restitution
            a.vel = v - (1 + restitution) * v_n * info.normal
        return
    
    relative_vel = b.vel - a.vel
    vel_along_normal = np.dot(relative_vel, info.normal)
    
    if vel_along_normal > 0:
        return
    
    restitution = min(a.restitution, b.restitution)
    j = -(1 + restitution) * vel_along_normal
    j /= a.inv_mass + b.inv_mass
    
    impulse = j * info.normal
    a.apply_impulse(-impulse)
    b.apply_impulse(impulse)
    
    percent = 0.2
    correction = (info.penetration / (a.inv_mass + b.inv_mass)) * percent * info.normal
    a.pos -= correction * a.inv_mass
    b.pos += correction * b.inv_mass 