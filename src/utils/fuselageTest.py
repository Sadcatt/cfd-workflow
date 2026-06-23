# also hallucinations from copilot, apparently makes stls??
from fuselage import fuselage as f
import gmsh
fuselage = f()
#print(nosecone.noseconePoints)


"""Generate a simple fuselage (nosecone + cylindrical body) and save as ASCII STL.

Creates a rotationally-symmetric fuselage by revolving a 2D profile.
No external dependencies required.

Output: fuselage.stl in the current working directory.
"""
import math


def generate_profile(nose_length=2.0, radius=0.5, body_length=6.0, nose_points=40, body_points=40):
    """Return list of (x, r) profile points from nose tip (x=0) to tail (x=total length).
    nose_length: length of nosecone
    radius: maximum radius (also cylinder radius)
    body_length: length of cylindrical section
    """
    pts = []
    # Nose profile: use half-ellipse for smooth nose (x from 0..nose_length)
    for i in range(nose_points):
        t = i / float(nose_points - 1)
        x = t * nose_length
        # half-ellipse: r = radius * sqrt(1 - ((x - nose_length)/nose_length)^2)
        # shift so tip at x=0: center at x=nose_length
        r = radius * math.sqrt(max(0.0, 1.0 - ((x - nose_length) / nose_length) ** 2))
        pts.append((x, r))

    # Body profile: straight cylinder
    start_x = nose_length
    for i in range(1, body_points + 1):
        t = i / float(body_points)
        x = start_x + t * body_length
        pts.append((x, radius))

    return pts


def revolve_profile_to_mesh(profile, segments=64):
    """Revolve profile around x-axis to create triangular mesh.
    Returns list of triangles, each triangle is ((x,y,z), ...)
    """
    # Create vertex grid: for each profile point and each angular segment
    verts = []
    for x, r in profile:
        ring = []
        for j in range(segments):
            theta = 2.0 * math.pi * j / segments
            y = r * math.cos(theta)
            z = r * math.sin(theta)
            ring.append((x, y, z))
        verts.append(ring)

    tris = []
    n_rings = len(verts)
    for i in range(n_rings - 1):
        A = verts[i]
        B = verts[i + 1]
        for j in range(segments):
            nj = (j + 1) % segments
            # two triangles per quad
            tris.append((A[j], B[j], B[nj]))
            tris.append((A[j], B[nj], A[nj]))

    # Cap the nose tip if radius at first profile point is zero
    if abs(profile[0][1]) < 1e-8:
        tip = verts[0][0]  # all ring verts coincide at tip
        ring1 = verts[1]
        for j in range(segments):
            nj = (j + 1) % segments
            tris.append((tip, ring1[nj], ring1[j]))

    return tris


def write_ascii_stl(filename, triangles, name="fuselage"):
    with open(filename, "w") as f:
        f.write(f"solid {name}\n")
        for tri in triangles:
            # compute normal
            (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = tri
            ux, uy, uz = x2 - x1, y2 - y1, z2 - z1
            vx, vy, vz = x3 - x1, y3 - y1, z3 - z1
            nx = uy * vz - uz * vy
            ny = uz * vx - ux * vz
            nz = ux * vy - uy * vx
            norm_len = math.sqrt(nx * nx + ny * ny + nz * nz)
            if norm_len > 0:
                nx, ny, nz = nx / norm_len, ny / norm_len, nz / norm_len
            else:
                nx = ny = nz = 0.0
            f.write(f"  facet normal {nx:.6e} {ny:.6e} {nz:.6e}\n")
            f.write("    outer loop\n")
            for vx, vy, vz in tri:
                f.write(f"      vertex {vx:.6e} {vy:.6e} {vz:.6e}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write(f"endsolid {name}\n")


def main():
    # Sensible default sizes (meters): nose 2m, radius 0.5m, body 6m
    profile = generate_profile(nose_length=2.0, radius=0.5, body_length=6.0, nose_points=40, body_points=80)
    tris = revolve_profile_to_mesh(profile, segments=96)
    out = "fuselage.stl"
    write_ascii_stl(out, tris)
    print(f"Wrote fuselage mesh to {out} (triangles: {len(tris)})")


if __name__ == "__main__":
    main()
