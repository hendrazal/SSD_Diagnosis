import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_c45_tree(tree, filename, figsize=(24, 14)):
    """
    Menggambar struktur pohon keputusan C4.5 kustom menggunakan Matplotlib
    dan menyimpannya sebagai file gambar PNG.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")

    # In-order traversal untuk mendaftarkan node dan menentukan koordinat X
    nodes_in_order = []
    node_depths = {}
    
    def traverse(node, depth):
        if node is None:
            return
        node_depths[node] = depth
        traverse(node.left, depth + 1)
        nodes_in_order.append(node)
        traverse(node.right, depth + 1)
        
    traverse(tree.root, 0)
    
    if not nodes_in_order:
        plt.text(0.5, 0.5, "Pohon keputusan kosong.", ha="center", va="center", fontsize=14)
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close()
        return

    # Hitung pemetaan indeks koordinat X dan kedalaman koordinat Y
    N = len(nodes_in_order)
    node_x = {node: i for i, node in enumerate(nodes_in_order)}
    max_depth = max(node_depths.values()) if node_depths else 1
    
    def get_coords(node):
        x = 0.05 + 0.9 * (node_x[node] / (N - 1)) if N > 1 else 0.5
        y = 0.95 - 0.9 * (node_depths[node] / max_depth) if max_depth > 0 else 0.5
        return x, y

    # Gambar cabang (garis penghubung) diagonal
    def draw_connections(node):
        if node is None or (node.left is None and node.right is None):
            return
        x, y = get_coords(node)
        
        threshold = math.ceil(node.threshold)
        
        if node.left is not None:
            lx, ly = get_coords(node.left)
            ax.plot([x, lx], [y, ly], color="#7F8C8D", linewidth=1.5, zorder=1)
            mx, my = (x + lx) / 2.0, (y + ly) / 2.0
            ax.text(mx, my, f"≤ {threshold}", fontsize=8, color="#2C3E50", fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#BDC3C7", alpha=0.9),
                    ha="center", va="center")
            draw_connections(node.left)
            
        if node.right is not None:
            rx, ry = get_coords(node.right)
            ax.plot([x, rx], [y, ry], color="#7F8C8D", linewidth=1.5, zorder=1)
            mx, my = (x + rx) / 2.0, (y + ry) / 2.0
            ax.text(mx, my, f"> {threshold}", fontsize=8, color="#2C3E50", fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#BDC3C7", alpha=0.9),
                    ha="center", va="center")
            draw_connections(node.right)

    # Gambar node (kotak teks)
    def draw_nodes(node):
        if node is None:
            return
        x, y = get_coords(node)
        
        if node.label is not None:
            label_text = f"LEAF: {node.label}\nSamples: {node.samples}\nConf: {node.probability * 100:.2f}%"
            color = "#2ECC71" if node.label == "Normal" else "#E74C3C"
            ax.text(x, y, label_text, fontsize=9, fontweight="bold", color="#FFFFFF",
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=color, edgecolor="#FFFFFF", alpha=0.95),
                    ha="center", va="center", zorder=2)
        else:
            feature_name = node.attribute.replace("_", " ")
            node_text = f"{feature_name}\n≤ {math.ceil(node.threshold)}?"
            ax.text(x, y, node_text, fontsize=9, fontweight="bold", color="#2C3E50",
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="#ECF0F1", edgecolor="#2C3E50", alpha=1.0),
                    ha="center", va="center", zorder=2)
            
            draw_nodes(node.left)
            draw_nodes(node.right)

    draw_connections(tree.root)
    draw_nodes(tree.root)
    
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
