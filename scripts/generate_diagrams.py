import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs("research/diagrams", exist_ok=True)

# 1. AI vs ML vs DL Nesting Dolls
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Outer: AI
p_ai = patches.FancyBboxPatch((0.5, 0.5), 9.0, 9.0, boxstyle="round,pad=0.3", ec="#1f77b4", fc="#e6f2ff", lw=3)
ax.add_patch(p_ai)
ax.text(5.0, 9.0, "1. ARTIFICIAL INTELLIGENCE (AI)", fontsize=14, fontweight='bold', ha='center', color="#0d47a1")
ax.text(5.0, 8.4, "Any system exhibiting smart behavior (Rules, Heuristics, Search, Game AI)", fontsize=10, ha='center', color="#333333")

# Middle: ML
p_ml = patches.FancyBboxPatch((1.2, 1.0), 7.6, 6.8, boxstyle="round,pad=0.3", ec="#2ca02c", fc="#eafaf1", lw=2.5)
ax.add_patch(p_ml)
ax.text(5.0, 7.3, "2. MACHINE LEARNING (ML)", fontsize=13, fontweight='bold', ha='center', color="#1b5e20")
ax.text(5.0, 6.7, "Learns patterns from data without explicit hardcoded rules\n(Regression, Decision Trees, Random Forests, Clustering)", fontsize=9.5, ha='center', color="#333333")

# Inner: DL
p_dl = patches.FancyBboxPatch((2.0, 1.5), 6.0, 4.6, boxstyle="round,pad=0.3", ec="#d62728", fc="#fdedec", lw=2.5)
ax.add_patch(p_dl)
ax.text(5.0, 5.5, "3. DEEP LEARNING (DL)", fontsize=12, fontweight='bold', ha='center', color="#b71c1c")
ax.text(5.0, 4.8, "Multi-layered Artificial Neural Networks\nDiscovers raw features automatically from unstructured data", fontsize=9.5, ha='center', color="#333333")
ax.text(5.0, 3.8, "Transformers (GPT, Llama, Qwen)\nConvolutional Nets (CNNs, Vision)\nDiffusion Models (Stable Diffusion, Flux)\nSelective SSMs (Mamba)", fontsize=9, ha='center', style='italic', color="#4a148c")

plt.tight_layout()
plt.savefig("research/diagrams/ai_ml_dl_nesting_dolls.png", bbox_inches='tight')
plt.close()

# 2. Radar Threat Clustering (K-Means Spartan Analogy)
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
np.random.seed(42)

# Grunts: Low armor, High/Medium speed
grunts_x = np.random.normal(0.25, 0.05, 30)
grunts_y = np.random.normal(0.75, 0.08, 30)
ax.scatter(grunts_x, grunts_y, color='#e67e22', s=60, label='Grunt Swarm (Cluster 1)', alpha=0.8)

# Jackals: Medium armor, Snipers
jackals_x = np.random.normal(0.45, 0.06, 20)
jackals_y = np.random.normal(0.40, 0.08, 20)
ax.scatter(jackals_x, jackals_y, color='#3498db', s=80, marker='^', label='Jackal Snipers (Cluster 2)', alpha=0.8)

# Hunters: Heavy armor, Low speed
hunters_x = np.random.normal(0.85, 0.05, 12)
hunters_y = np.random.normal(0.20, 0.05, 12)
ax.scatter(hunters_x, hunters_y, color='#2c3e50', s=140, marker='s', label='Mgalekgolo Hunters (Cluster 3)', alpha=0.9)

# Zealots: High armor, High speed
zealots_x = np.random.normal(0.75, 0.06, 15)
zealots_y = np.random.normal(0.85, 0.06, 15)
ax.scatter(zealots_x, zealots_y, color='#9b59b6', s=100, marker='D', label='Elite Zealots (Cluster 4)', alpha=0.85)

ax.axvline(0.5, color='gray', linestyle='--', alpha=0.4)
ax.axhline(0.5, color='gray', linestyle='--', alpha=0.4)

ax.set_title("Master Chief HUD: Unsupervised Threat Radar Clustering (K-Means)", fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel("Armor Thickness / Defense Factor (Low -> Heavy)", fontsize=11)
ax.set_ylabel("Speed / Agility Profile (Low -> High)", fontsize=11)
ax.set_xlim(0, 1.05)
ax.set_ylim(0, 1.05)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='lower left', framealpha=0.9)

plt.tight_layout()
plt.savefig("research/diagrams/spartan_ml_radar_clustering.png", bbox_inches='tight')
plt.close()

# 3. Roofline Model: Arithmetic Intensity & Silicon Bottlenecks
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
I = np.logspace(-1, 3, 500)
P_peak = 2000.0  # TFLOPS (H100)
B_mem = 3.35     # TB/s
# P = min(P_peak, I * B_mem)
P = np.minimum(P_peak, I * (B_mem * 1000 / 1000)) # scaled for TFLOPS

ax.plot(I, np.minimum(P_peak, I * 335), color='#d35400', lw=3, label='NVIDIA H100 Roofline (3.35 TB/s, ~2000 TFLOPS)')
ax.axhline(P_peak, color='gray', linestyle=':', label='Peak Compute Ceiling (P_peak)')

# Highlight Regions
ax.axvspan(0.1, 6.0, color='#fdebd0', alpha=0.5, label='Memory-Bandwidth Bound (Autoregressive Decode)')
ax.axvspan(6.0, 1000, color='#d4efdf', alpha=0.5, label='Compute-Bound (Training & Prefill)')

# Annotations
ax.scatter([1.5], [1.5 * 335], color='red', s=100, zorder=5)
ax.annotate('Token Decode (GEMV)\nI ≈ 1-2 FLOPs/Byte\n(Memory Wall Bottleneck)', 
            xy=(1.5, 1.5 * 335), xytext=(0.2, 800),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
            fontsize=9.5, fontweight='bold', bbox=dict(boxstyle="round", fc="white", ec="red"))

ax.scatter([100], [P_peak], color='green', s=100, zorder=5)
ax.annotate('Prompt Prefill (GEMM)\nI > 50 FLOPs/Byte\n(Max Tensor Core Utilization)', 
            xy=(100, P_peak), xytext=(40, 1200),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
            fontsize=9.5, fontweight='bold', bbox=dict(boxstyle="round", fc="white", ec="green"))

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_title("Roofline Model: Arithmetic Intensity & The Memory Wall in LLMs", fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel("Arithmetic Intensity: FLOPs / Byte Accessed (log scale)", fontsize=11)
ax.set_ylabel("Attainable Performance: TFLOPS (log scale)", fontsize=11)
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend(loc='lower right', framealpha=0.9, fontsize=9)

plt.tight_layout()
plt.savefig("research/diagrams/ml_hardware_roofline.png", bbox_inches='tight')
plt.close()

# 4. Master Chief LAN Topology
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Box 1: M1 iMac (Controller)
p_m1 = patches.FancyBboxPatch((0.5, 3.8), 4.2, 3.6, boxstyle="round,pad=0.2", ec="#2980b9", fc="#ebf5fb", lw=2)
ax.add_patch(p_m1)
ax.text(2.6, 7.0, "CHRIS iMAC M1 (16GB UMA)", fontsize=11, fontweight='bold', ha='center', color="#1a5276")
ax.text(2.6, 6.4, "Role: Field Commander / Operator Desk", fontsize=9, ha='center')
ax.text(2.6, 5.7, "• Master Chief Electron UI\n• Classical ML Intent Gate (<5ms)\n• Ollama (Qwen-3 8B @ Q4_K_M)\n• HTTP MCP Tool Bus Client", fontsize=8.5, ha='center', color="#2c3e50")
ax.text(2.6, 4.3, "IP: 192.168.4.42 | Port: 11434", fontsize=8, ha='center', style='italic', color="#7f8c8d")

# Box 2: AMD Comfy (Media Forge)
p_amd = patches.FancyBboxPatch((5.3, 3.8), 4.2, 3.6, boxstyle="round,pad=0.2", ec="#c0392b", fc="#fdedec", lw=2)
ax.add_patch(p_amd)
ax.text(7.4, 7.0, "WINDOWS AMD BOX", fontsize=11, fontweight='bold', ha='center', color="#922b21")
ax.text(7.4, 6.4, "Role: Media Forge (Creative Worker)", fontsize=9, ha='center')
ax.text(7.4, 5.7, "• ComfyUI Server (:8188)\n• SDXL / Flux Image Synthesis\n• LoRA Adapters & Video Gen\n• Dedicated Compute Matrix", fontsize=8.5, ha='center', color="#2c3e50")
ax.text(7.4, 4.3, "IP: 192.168.4.20 | Port: 8188", fontsize=8, ha='center', style='italic', color="#7f8c8d")

# Box 3: Sarah M3 (Spillover)
p_m3 = patches.FancyBboxPatch((0.5, 0.4), 4.2, 2.6, boxstyle="round,pad=0.2", ec="#8e44ad", fc="#f4ecf7", lw=1.5, linestyle="--")
ax.add_patch(p_m3)
ax.text(2.6, 2.6, "SARAH iMAC M3 (Phase E)", fontsize=10, fontweight='bold', ha='center', color="#5b2c6f")
ax.text(2.6, 2.0, "Role: Heavy Compute Reserve", fontsize=8.5, ha='center')
ax.text(2.6, 1.3, "• Spillover Ollama Node\n• 14B-32B Reasoning Models\n• 60% Faster Memory Bandwidth", fontsize=8, ha='center', color="#2c3e50")

# Box 4: Tools Substrate
p_tools = patches.FancyBboxPatch((5.3, 0.4), 4.2, 2.6, boxstyle="round,pad=0.2", ec="#27ae60", fc="#eafaf1", lw=2)
ax.add_patch(p_tools)
ax.text(7.4, 2.6, "HTTP MCP TOOL BUS", fontsize=10, fontweight='bold', ha='center', color="#196f3d")
ax.text(7.4, 2.0, "Role: System Connectors & APIs", fontsize=8.5, ha='center')
ax.text(7.4, 1.3, "• Notes / Recipe Filesystem MCP\n• LAN Health & Node Status MCP\n• Git Repo / GitHub Read MCP", fontsize=8, ha='center', color="#2c3e50")

# Connecting Arrows
ax.annotate('', xy=(5.3, 5.6), xytext=(4.7, 5.6), arrowprops=dict(arrowstyle="<->", lw=2, color="#e67e22"))
ax.text(5.0, 5.9, "HTTP LAN (1 Gbps)", fontsize=8, ha='center', fontweight='bold', color="#d35400")

ax.annotate('', xy=(7.4, 3.8), xytext=(7.4, 3.0), arrowprops=dict(arrowstyle="<-", lw=1.5, color="#27ae60"))
ax.annotate('', xy=(2.6, 3.8), xytext=(2.6, 3.0), arrowprops=dict(arrowstyle="<->", lw=1.5, linestyle="--", color="#8e44ad"))

plt.suptitle("Master Chief Hologram: Household LAN Architecture", fontsize=13, fontweight='bold', y=0.96)
plt.tight_layout()
plt.savefig("research/diagrams/master_chief_lan_topology.png", bbox_inches='tight')
plt.close()

# 5. Voice Latency Pipeline (Batch vs Streaming)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 4.5), dpi=300)

# Batch
ax1.barh(["Batch Architecture\n(Total ~3,200 ms)"], [600], color='#e74c3c', label='User Speaks')
ax1.barh(["Batch Architecture\n(Total ~3,200 ms)"], [500], left=[600], color='#e67e22', label='Whisper STT')
ax1.barh(["Batch Architecture\n(Total ~3,200 ms)"], [1500], left=[1100], color='#f1c40f', label='Ollama Full Decode')
ax1.barh(["Batch Architecture\n(Total ~3,200 ms)"], [600], left=[2600], color='#9b59b6', label='TTS Synthesis')
ax1.set_xlim(0, 3500)
ax1.set_xlabel("Latency in Milliseconds (ms)", fontsize=9)
ax1.set_title("Standard Sequential Pipeline (High Conversational Lag)", fontsize=10, fontweight='bold')
ax1.legend(loc='lower right', fontsize=8, ncol=4)

# Streaming
ax2.barh(["Bland-Style Streaming\n(Audio at ~650 ms)"], [500], color='#2ecc71', label='VAD Trigger')
ax2.barh(["Bland-Style Streaming\n(Audio at ~650 ms)"], [150], left=[500], color='#3498db', label='Sentence 1 Token')
ax2.barh(["Bland-Style Streaming\n(Audio at ~650 ms)"], [150], left=[650], color='#1abc9c', label='Stream Audio Chunk')
ax2.set_xlim(0, 3500)
ax2.set_xlabel("Latency in Milliseconds (ms)", fontsize=9)
ax2.set_title("Optimized Streaming Pipeline (Sub-Second Natural Voice Interactivity)", fontsize=10, fontweight='bold')
ax2.legend(loc='lower right', fontsize=8, ncol=3)

plt.tight_layout()
plt.savefig("research/diagrams/bland_voice_latency_pipeline.png", bbox_inches='tight')
plt.close()

print("Successfully generated all high-resolution research PNG diagrams!")
