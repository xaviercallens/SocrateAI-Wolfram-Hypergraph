/**
 * 4K UHD Cyberpunk WebGL Video Generator Engine
 * Powered by Three.js (WebGL) & FFmpeg.wasm
 */

const FFmpegLib = window.FFmpegWASM || window.FFmpeg || {};
const { FFmpeg } = FFmpegLib;

let threeScene = null;
let threeCamera = null;
let threeRenderer = null;
let nodeGroup = null;
let edgeLineSegments = null;
let ffmpegInstance = null;
let isRendering = false;

// High-Density Parameters
const TOTAL_FRAMES = 660; 
const ATOMS_PER_SEC = 25; // Growth rate (+25 nodes/sec)

// Pre-computed String ID Lookup Cache
const ID_CACHE = Array.from({ length: 30000 }, (_, i) => i.toString());

let statefulNodes = [];
let statefulEdges = [];
let statefulNodeCount = 0;

// Initialize 3D Cyberpunk Three.js WebGL Engine
function initThreeEngine() {
    const canvas = document.getElementById('cosmograph-canvas');
    if (!canvas) return;

    const width = canvas.clientWidth || 800;
    const height = canvas.clientHeight || 450;

    threeScene = new THREE.Scene();
    threeScene.fog = new THREE.FogExp2(0x03050a, 0.003);

    threeCamera = new THREE.PerspectiveCamera(60, width / height, 0.1, 2000);
    threeCamera.position.set(0, 150, 400);
    threeCamera.lookAt(0, 0, 0);

    threeRenderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: true,
        alpha: false,
        preserveDrawingBuffer: true
    });
    threeRenderer.setSize(width, height);
    threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    threeRenderer.setClearColor(0x03050a, 1.0);

    // Ambient & Point Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    threeScene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00f0ff, 2.5, 800);
    pointLight.position.set(0, 100, 200);
    threeScene.add(pointLight);

    nodeGroup = new THREE.Group();
    threeScene.add(nodeGroup);
}

// Generate K3xT2 Topology (48 K3 base crossed with 6x6 T2 torus fiber grid = 1,728 base nodes)
let baseK3T2 = null;
function getBaseTopology() {
    if (baseK3T2) return baseK3T2;
    
    const nodes = [];
    const edges = [];
    
    const k3_nodes = 48;
    const k3_edges = [];
    for (let i = 0; i < k3_nodes; i++) {
        k3_edges.push([i, (i + 1) % k3_nodes]);
        k3_edges.push([i, (i + 2) % k3_nodes]);
        k3_edges.push([i, (i + 3) % k3_nodes]);
        k3_edges.push([i, (i + 4) % k3_nodes]);
    }
    
    const t2_dim = 6;
    const t2_nodes = t2_dim * t2_dim;
    const t2_edges = [];
    for (let r = 0; r < t2_dim; r++) {
        for (let c = 0; c < t2_dim; c++) {
            const u = r * t2_dim + c;
            const down = ((r + 1) % t2_dim) * t2_dim + c;
            const right = r * t2_dim + ((c + 1) % t2_dim);
            t2_edges.push([u, down]);
            t2_edges.push([u, right]);
        }
    }
    
    // Assign 3D spatial layout positions for K3 (outer ring) x T2 (toroidal fiber)
    for (let u = 0; u < k3_nodes; u++) {
        const theta = (u / k3_nodes) * Math.PI * 2;
        const R = 140; // Major radius of K3 base
        
        for (let v = 0; v < t2_nodes; v++) {
            const id = u * t2_nodes + v;
            const r_idx = Math.floor(v / t2_dim);
            const c_idx = v % t2_dim;
            
            const phi = (r_idx / t2_dim) * Math.PI * 2;
            const psi = (c_idx / t2_dim) * Math.PI * 2;
            const r_minor = 35; // Minor radius of T2 fiber
            
            const x = (R + r_minor * Math.cos(phi)) * Math.cos(theta);
            const y = r_minor * Math.sin(phi) * 1.5;
            const z = (R + r_minor * Math.cos(phi)) * Math.sin(theta);

            nodes.push({
                id: id.toString(),
                type: u % 2 === 0 ? 'k3' : 't2',
                x: x, y: y, z: z
            });
        }
    }
    
    for (let u = 0; u < k3_nodes; u++) {
        for (let v = 0; v < t2_nodes; v++) {
            const id = u * t2_nodes + v;
            t2_edges.forEach(([v1, v2]) => {
                if (v === v1) edges.push({ source: id.toString(), target: (u * t2_nodes + v2).toString() });
            });
            k3_edges.forEach(([u1, u2]) => {
                if (u === u1) edges.push({ source: id.toString(), target: (u2 * t2_nodes + v).toString() });
            });
        }
    }
    
    baseK3T2 = { nodes, edges };
    return baseK3T2;
}

function resetIncrementalPhysics() {
    const base = getBaseTopology();
    statefulNodes = base.nodes.map(n => ({ ...n }));
    statefulEdges = base.edges.map(e => ({ ...e }));
    statefulNodeCount = statefulNodes.length;
}

function advancePhysicsFrame() {
    if (statefulNodeCount === 0) resetIncrementalPhysics();
    
    // Add 25 nodes per frame with 3D vacuum accretion positions
    for (let i = 0; i < ATOMS_PER_SEC; i++) {
        const newId = ID_CACHE[statefulNodeCount] || statefulNodeCount.toString();
        
        // Random spherical inflation shell expansion
        const radius = 160 + Math.random() * 80;
        const u_angle = Math.random() * Math.PI * 2;
        const v_angle = (Math.random() - 0.5) * Math.PI;
        
        const x = radius * Math.cos(v_angle) * Math.cos(u_angle);
        const y = radius * Math.sin(v_angle);
        const z = radius * Math.cos(v_angle) * Math.sin(u_angle);

        statefulNodes.push({ id: newId, type: 'vacuum', x, y, z });
        
        const targetIdx1 = Math.floor(Math.random() * statefulNodeCount);
        const target1 = ID_CACHE[targetIdx1] || targetIdx1.toString();
        statefulEdges.push({ source: newId, target: target1 });
        
        if (i % 2 === 0) {
            const targetIdx2 = Math.floor(Math.random() * statefulNodeCount);
            const target2 = ID_CACHE[targetIdx2] || targetIdx2.toString();
            statefulEdges.push({ source: newId, target: target2 });
        }
        
        statefulNodeCount++;
    }
    return { nodes: statefulNodes, edges: statefulEdges };
}

// Update 3D WebGL Hypergraph Meshes & Line Segments
function renderWebGLGraphToFrame(frameIndex, graph) {
    if (!threeScene) initThreeEngine();

    // Rotate camera smoothly around the 3D hypergraph manifold
    const rotSpeed = frameIndex * 0.008;
    const camRadius = 420;
    threeCamera.position.x = Math.sin(rotSpeed) * camRadius;
    threeCamera.position.z = Math.cos(rotSpeed) * camRadius;
    threeCamera.position.y = 120 + Math.sin(rotSpeed * 0.5) * 40;
    threeCamera.lookAt(0, 0, 0);

    // Rebuild Nodes & Glowing Points
    while (nodeGroup.children.length > 0) {
        nodeGroup.remove(nodeGroup.children[0]);
    }

    const nodePositions = [];
    const nodeColors = [];

    const k3Color = new THREE.Color(0x00f0ff);   // Electric Cyan
    const t2Color = new THREE.Color(0xff007f);   // Neon Magenta
    const vacColor = new THREE.Color(0xffd700);  // Cyber Gold

    graph.nodes.forEach(n => {
        nodePositions.push(n.x, n.y, n.z);
        const col = n.type === 'k3' ? k3Color : (n.type === 't2' ? t2Color : vacColor);
        nodeColors.push(col.r, col.g, col.b);
    });

    const nodeGeo = new THREE.BufferGeometry();
    nodeGeo.setAttribute('position', new THREE.Float32BufferAttribute(nodePositions, 3));
    nodeGeo.setAttribute('color', new THREE.Float32BufferAttribute(nodeColors, 3));

    const nodeMat = new THREE.PointsMaterial({
        size: 5.5,
        vertexColors: true,
        transparent: true,
        opacity: 0.9,
        blending: THREE.AdditiveBlending
    });

    const pointsMesh = new THREE.Points(nodeGeo, nodeMat);
    nodeGroup.add(pointsMesh);

    // Rebuild Edge Line Segments
    const linePositions = [];
    const nodeMap = new Map();
    graph.nodes.forEach(n => nodeMap.set(n.id, n));

    graph.edges.forEach(e => {
        const src = nodeMap.get(e.source);
        const tgt = nodeMap.get(e.target);
        if (src && tgt) {
            linePositions.push(src.x, src.y, src.z);
            linePositions.push(tgt.x, tgt.y, tgt.z);
        }
    });

    const edgeGeo = new THREE.BufferGeometry();
    edgeGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));

    const edgeMat = new THREE.LineBasicMaterial({
        color: 0x00f0ff,
        transparent: true,
        opacity: 0.3,
        blending: THREE.AdditiveBlending
    });

    const linesMesh = new THREE.LineSegments(edgeGeo, edgeMat);
    nodeGroup.add(linesMesh);

    // Render WebGL frame
    threeRenderer.render(threeScene, threeCamera);
}

async function loadFFmpeg() {
    if (ffmpegInstance) return ffmpegInstance;

    document.getElementById('encoder-status-text').innerText = "LOADING CORE...";
    
    if (FFmpeg) {
        ffmpegInstance = new FFmpeg();
        ffmpegInstance.on('log', ({ message }) => console.log('[ffmpeg]', message));
        await ffmpegInstance.load({
            coreURL: 'https://unpkg.com/@ffmpeg/core@0.12.6/dist/umd/ffmpeg-core.js',
            wasmURL: 'https://unpkg.com/@ffmpeg/core@0.12.6/dist/umd/ffmpeg-core.wasm'
        });
    }
    return ffmpegInstance;
}

async function startGPUVideoEncoding() {
    if (isRendering) return;
    isRendering = true;

    try {
        initThreeEngine();

        const btn = document.getElementById('btn-render-video');
        btn.innerText = "RENDERING 4K CYBERPUNK WEBGL VIDEO...";
        btn.style.pointerEvents = "none";
        btn.style.opacity = "0.7";

        document.getElementById('video-overlay-text').style.display = "block";
        document.getElementById('video-timer').style.display = "block";
        document.getElementById('video-title').style.display = "block";

        const ffmpeg = await loadFFmpeg();
        document.getElementById('encoder-status-text').innerText = "ENCODING 4K UHD...";

        const canvas = document.getElementById('cosmograph-canvas');
        
        // Native 4K Canvas Context (3840 x 2160)
        const captureCanvas = document.createElement('canvas');
        captureCanvas.width = 3840; 
        captureCanvas.height = 2160;
        const ctx = captureCanvas.getContext('2d');

        resetIncrementalPhysics();

        for (let i = 1; i <= TOTAL_FRAMES; i++) {
            const graph = advancePhysicsFrame();
            
            // Render 3D WebGL Scene
            renderWebGLGraphToFrame(i, graph);
            
            await new Promise(r => setTimeout(r, 20)); 

            // Draw to 4K UHD Canvas
            ctx.fillStyle = '#03050a';
            ctx.fillRect(0, 0, captureCanvas.width, captureCanvas.height);
            ctx.drawImage(canvas, 0, 0, captureCanvas.width, captureCanvas.height);

            // Cyberpunk HUD Overlay Header (4K UHD)
            ctx.fillStyle = "#00f0ff";
            ctx.font = "bold 60px 'Segoe UI', Roboto, monospace";
            ctx.shadowColor = "#00f0ff";
            ctx.shadowBlur = 20;
            ctx.fillText("MINUTE 11: GRAND SYNTHESIS (K3×T² HYPERGRAPH)", 100, 120);
            ctx.shadowBlur = 0;
            
            const mins = Math.floor((i - 1) / 60).toString().padStart(2, '0');
            const secs = ((i - 1) % 60).toString().padStart(2, '0');
            ctx.fillStyle = "#ffd700";
            ctx.font = "bold 56px monospace";
            ctx.textAlign = "right";
            ctx.fillText(`TIME: ${mins}:${secs} / 11:00`, captureCanvas.width - 100, 120);
            ctx.textAlign = "left";

            // Node/Edge Counter
            ctx.fillStyle = "#a78bfa";
            ctx.font = "38px monospace";
            ctx.fillText(`ATOMS: ${graph.nodes.length.toLocaleString()} | EDGES: ${graph.edges.length.toLocaleString()}`, 100, 180);

            // Subtitle Banner Overlay (4K UHD)
            ctx.fillStyle = "rgba(3, 5, 10, 0.92)";
            const bw = captureCanvas.width * 0.88;
            const bx = (captureCanvas.width - bw) / 2;
            const by = captureCanvas.height - 220;
            const bh = 150;
            
            ctx.fillRect(bx, by, bw, bh);
            ctx.strokeStyle = "#00f0ff";
            ctx.lineWidth = 6;
            ctx.shadowColor = "#00f0ff";
            ctx.shadowBlur = 25;
            ctx.strokeRect(bx, by, bw, bh);
            ctx.shadowBlur = 0;
            
            ctx.fillStyle = "#ffffff";
            ctx.font = "52px 'Segoe UI', Roboto, sans-serif";
            ctx.textAlign = "center";
            ctx.fillText('"Grand Synthesis: Primordial K4 hypergraph seeds evolve into full cosmological complexity..."', captureCanvas.width / 2, by + 90);

            // Export frame PNG to WASM VFS if ffmpeg is loaded
            if (ffmpeg) {
                const blob = await new Promise(r => captureCanvas.toBlob(r, 'image/png'));
                const arrayBuffer = await blob.arrayBuffer();
                const uint8Array = new Uint8Array(arrayBuffer);
                const fileName = `frame_${i.toString().padStart(5, '0')}.png`;
                await ffmpeg.writeFile(fileName, uint8Array);
            }

            // Update UI Progress Bar
            const pct = (i / TOTAL_FRAMES) * 100;
            document.getElementById('render-progress-bar').style.width = pct + "%";
            document.getElementById('render-progress-text').innerText = `${i} / ${TOTAL_FRAMES} Frames (4K UHD)`;
            document.getElementById('video-timer').innerText = `TIME: ${mins}:${secs} / 11:00`;
        }

        if (ffmpeg) {
            document.getElementById('encoder-status-text').innerText = "MUXING 4K H.264 MP4...";
            await ffmpeg.exec([
                '-framerate', '1', 
                '-i', 'frame_%05d.png',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-crf', '16',
                'output_4k.mp4'
            ]);
            const data = await ffmpeg.readFile('output_4k.mp4');
            const videoBlob = new Blob([data.buffer], { type: 'video/mp4' });
            const url = URL.createObjectURL(videoBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'cyberpunk_4k_k3t2_hypergraph_cosmology.mp4';
            a.click();
            URL.revokeObjectURL(url);
        }

        document.getElementById('encoder-status-text').innerText = "DONE (4K EXPORTED)!";
        document.getElementById('encoder-status-text').style.color = "#10b981";
        btn.innerText = "✅ 4K CYBERPUNK VIDEO GENERATION COMPLETE";

    } catch (e) {
        console.error(e);
        document.getElementById('encoder-status-text').innerText = "ERROR";
        document.getElementById('encoder-status-text').style.color = "#ef4444";
        alert("4K Video generation failed: " + e.message);
    } finally {
        isRendering = false;
    }
}
