import os
import math
import random
import sys
import subprocess
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont

# Path Resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
STATIC_DIR = os.path.join(WORKSPACE, "dashboard", "frontend")
os.makedirs(STATIC_DIR, exist_ok=True)
OUTPUT_MP4 = os.path.join(STATIC_DIR, "cyberpunk_4k_k3t2_hypergraph_cosmology.mp4")

# Parameters
TOTAL_FRAMES = 660
ATOMS_PER_SEC = 25
WIDTH = 3840
HEIGHT = 2160
FOV = 60.0  # Field of View in degrees

# Colors
BG_COLOR = (3, 5, 10, 255)       # Cyber Black
CYAN = (0, 240, 255, 255)        # Electric Cyan
MAGENTA = (255, 0, 127, 255)     # Neon Magenta
GOLD = (255, 215, 0, 255)        # Cyber Gold
WHITE = (255, 255, 255, 255)
BANNER_BG = (3, 5, 10, 235)      # Translucent Dark Glass

# Math: Vector operations
def normalize(v):
    mag = math.sqrt(sum(x*x for x in v))
    if mag == 0:
        return [0.0, 0.0, 0.0]
    return [x / mag for x in v]

def cross(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

# Generate Base Topology (1,728 nodes)
def get_base_topology():
    nodes = []
    edges = []
    k3_nodes = 48
    t2_dim = 6
    t2_nodes = t2_dim * t2_dim

    k3_edges = []
    for i in range(k3_nodes):
        k3_edges.append([i, (i + 1) % k3_nodes])
        k3_edges.append([i, (i + 2) % k3_nodes])
        k3_edges.append([i, (i + 3) % k3_nodes])
        k3_edges.append([i, (i + 4) % k3_nodes])

    t2_edges = []
    for r in range(t2_dim):
        for c in range(t2_dim):
            u = r * t2_dim + c
            down = ((r + 1) % t2_dim) * t2_dim + c
            right = r * t2_dim + ((c + 1) % t2_dim)
            t2_edges.append([u, down])
            t2_edges.append([u, right])

    for u in range(k3_nodes):
        theta = (u / k3_nodes) * math.pi * 2
        R = 140.0
        for v in range(t2_nodes):
            id_val = u * t2_nodes + v
            r_idx = v // t2_dim
            c_idx = v % t2_dim
            phi = (r_idx / t2_dim) * math.pi * 2
            r_minor = 35.0

            x = (R + r_minor * math.cos(phi)) * math.cos(theta)
            y = r_minor * math.sin(phi) * 1.5
            z = (R + r_minor * math.cos(phi)) * math.sin(theta)

            nodes.append({
                "id": id_val,
                "type": "k3" if u % 2 == 0 else "t2",
                "x": x, "y": y, "z": z
            })

    for u in range(k3_nodes):
        for v in range(t2_nodes):
            id_val = u * t2_nodes + v
            for v1, v2 in t2_edges:
                if v == v1:
                    edges.append((id_val, u * t2_nodes + v2))
            for u1, u2 in k3_edges:
                if u == u1:
                    edges.append((id_val, u2 * t2_nodes + v))

    return nodes, edges

# Perspective 3D Projection
def project_point(p, cam_pos, forward, right, up, f_scale):
    v = [p[0] - cam_pos[0], p[1] - cam_pos[1], p[2] - cam_pos[2]]
    vx = dot(v, right)
    vy = dot(v, up)
    vz = dot(v, forward)

    if vz <= 10.0:
        return None

    x = (vx / vz) * f_scale * (HEIGHT / 2.0) + WIDTH / 2.0
    y = -(vy / vz) * f_scale * (HEIGHT / 2.0) + HEIGHT / 2.0
    return int(x), int(y)

# Render Single Frame (Worker Task)
def render_frame_worker(args):
    f_idx, nodes, edges, cam_pos, forward, right, up, f_scale, tmp_frame_dir = args

    # Initialize fonts inside worker process
    try:
        font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 52)
        font_mono = ImageFont.truetype("DejaVuSansMono-Bold.ttf", 44)
    except IOError:
        font_header = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_mono = ImageFont.load_default()

    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Project Coordinates
    projected = {}
    for n in nodes:
        coords = project_point([n["x"], n["y"], n["z"]], cam_pos, forward, right, up, f_scale)
        if coords:
            projected[n["id"]] = coords

    # Draw Edges
    edge_color = (0, 95, 105, 255)
    for u, v in edges:
        if u in projected and v in projected:
            draw.line([projected[u], projected[v]], fill=edge_color, width=2)

    # Draw Nodes
    for n in nodes:
        nid = n["id"]
        if nid not in projected:
            continue
        cx, cy = projected[nid]
        ntype = n["type"]

        if ntype == "k3":
            col = CYAN
        elif ntype == "t2":
            col = MAGENTA
        else:
            col = GOLD

        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=col)

    # HUD Overlays
    draw.text((100, 100), "MINUTE 11: GRAND SYNTHESIS (K3×T² HYPERGRAPH)", fill=CYAN, font=font_header)
    
    mins = (f_idx - 1) // 60
    secs = (f_idx - 1) % 60
    draw.text((WIDTH - 100, 100), f"TIME: {mins:02d}:{secs:02d} / 11:00", fill=GOLD, font=font_mono, anchor="ra")
    draw.text((100, 180), f"ATOMS: {len(nodes):,} | EDGES: {len(edges):,}", fill=MAGENTA, font=font_mono)

    # Subtitle Banner
    bw = int(WIDTH * 0.88)
    bx = int((WIDTH - bw) / 2)
    by = HEIGHT - 220
    bh = 150
    draw.rectangle([bx, by, bx + bw, by + bh], fill=BANNER_BG, outline=CYAN, width=6)
    draw.text((WIDTH // 2, by + 45), '"Grand Synthesis: Primordial K4 hypergraph seeds evolve into full cosmological complexity..."', fill=WHITE, font=font_sub, anchor="mm")

    # Save to temp file
    frame_path = os.path.join(tmp_frame_dir, f"frame_{f_idx:05d}.jpg")
    img.convert("RGB").save(frame_path, "JPEG", quality=95)
    return f_idx

def generate_video():
    print("🚀 Initializing Multiprocess 4K Video Generator...")
    base_nodes, base_edges = get_base_topology()
    
    tmp_frame_dir = os.path.join(WORKSPACE, "scratch", "4k_frames")
    os.makedirs(tmp_frame_dir, exist_ok=True)

    import imageio_ffmpeg
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

    # Pre-simulate all frame topologies deterministically
    print("🧠 Simulating all frame topologies...")
    random.seed(42)
    
    frames_data = []
    current_nodes = [dict(n) for n in base_nodes]
    current_edges = list(base_edges)

    for f_idx in range(1, TOTAL_FRAMES + 1):
        # Accrete atoms
        for _ in range(ATOMS_PER_SEC):
            radius = 160.0 + random.random() * 80.0
            u_angle = random.random() * math.pi * 2
            v_angle = (random.random() - 0.5) * math.pi
            
            x = radius * math.cos(v_angle) * math.cos(u_angle)
            y = radius * math.sin(v_angle)
            z = radius * math.cos(v_angle) * math.sin(u_angle)

            new_id = len(current_nodes)
            current_nodes.append({
                "id": new_id,
                "type": "vacuum",
                "x": x, "y": y, "z": z
            })

            target1 = random.randint(0, new_id - 1)
            current_edges.append((new_id, target1))
            if random.random() > 0.5:
                target2 = random.randint(0, new_id - 1)
                current_edges.append((new_id, target2))

        # Setup Camera Orbit
        rot_speed = f_idx * 0.008
        cam_radius = 420.0
        cam_x = math.sin(rot_speed) * cam_radius
        cam_z = math.cos(rot_speed) * cam_radius
        cam_y = 120.0 + math.sin(rot_speed * 0.5) * 40.0
        cam_pos = [cam_x, cam_y, cam_z]

        forward = normalize([-cam_x, -cam_y, -cam_z])
        right = normalize(cross(forward, [0.0, 1.0, 0.0]))
        up = normalize(cross(right, forward))
        f_scale = 1.0 / math.tan(math.radians(FOV / 2.0))

        # Save snapshot state for worker
        frames_data.append((
            f_idx,
            list(current_nodes),
            list(current_edges),
            cam_pos, forward, right, up, f_scale,
            tmp_frame_dir
        ))

    print(f"🎬 Rendering {TOTAL_FRAMES} frames in parallel across CPU cores...")
    # Use 8 processes to render frames concurrently
    with Pool(processes=8) as pool:
        results = pool.map(render_frame_worker, frames_data)
        print(f"✅ Rendered all {len(results)} frames successfully.")

    print("🎥 Muxing 4K UHD H.264 video with native FFmpeg...")
    cmd = [
        ffmpeg_bin, "-y",
        "-framerate", "1",
        "-i", os.path.join(tmp_frame_dir, "frame_%05d.jpg"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "16",
        OUTPUT_MP4
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✅ Video successfully cached at {OUTPUT_MP4}!")

    # Cleanup
    for f in os.listdir(tmp_frame_dir):
        os.remove(os.path.join(tmp_frame_dir, f))
    os.rmdir(tmp_frame_dir)

if __name__ == "__main__":
    generate_video()
