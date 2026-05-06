"""
P0-4 创新原型：液-液相分离启发的动态知识组织 (LLPS Knowledge Organization)

生物学基础：液-液相分离 (Liquid-Liquid Phase Separation)
 - 无膜细胞器：核仁、应激颗粒、P-body 通过蛋白-RNA 相分离自发形成
 - 动态组装：液滴可在秒-分钟级形成、融合、分裂、消散
 - 功能浓缩：液滴内分子浓度提升 100-1000 倍，反应效率显著提升
 - 相变阈值：浓度超过临界值时突然发生相分离

AI 缺口：Transformer O(n²) 注意力、静态知识图谱、固定嵌入空间
→ 缺乏动态、上下文依赖、自组织的知识聚类机制。

核心优势：O(n²) → O(k × m²)，k=液滴数，m=平均液滴大小。

纯 Python 实现，嵌入用 list[float] 表示。
"""
from __future__ import annotations

import math

# 类型别名
Vec = list[float]           # 嵌入向量
Matrix = list[list[float]]  # 矩阵


# ─── 向量运算工具（纯 Python） ─────────────────────────────────────────────

def dot(a: Vec, b: Vec) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(v: Vec) -> float:
    return math.sqrt(sum(x * x for x in v)) + 1e-8


def cosine(a: Vec, b: Vec) -> float:
    return dot(a, b) / (norm(a) * norm(b))


def vec_mean(vecs: list[Vec]) -> Vec:
    if not vecs:
        return []
    dim = len(vecs[0])
    return [sum(v[i] for v in vecs) / len(vecs) for i in range(dim)]


# ─── 知识液滴 ─────────────────────────────────────────────────────────────

class KnowledgeDroplet:
    """知识液滴：语义相关概念的动态聚集体（类比无膜细胞器）"""

    def __init__(self, droplet_id: int, core: list[int], boundary: list[int], centroid: Vec):
        # 核心概念：高密度区域，对应液滴中心的多价相互作用网络
        self.droplet_id = droplet_id
        self.core = core
        # 边界概念：与其他液滴交换信息的接口（类比液滴表面）
        self.boundary = boundary
        # 质心嵌入：液滴的语义中心
        self.centroid = centroid

    @property
    def members(self) -> list[int]:
        return self.core + self.boundary

    @property
    def size(self) -> int:
        return len(self.members)


# ─── 相分离检测 ───────────────────────────────────────────────────────────

class LLPSKnowledgeSystem:
    """液-液相分离启发的知识组织系统。

    工作流：嵌入 → 相分离 → 液滴形成 → 液滴内注意力 → 液滴融合/查询。
    """

    def __init__(
        self,
        density_threshold: float = 0.6,
        surface_tension: float = 0.5,
        min_droplet_size: int = 2,
        max_droplet_size: int = 50,
        neighbor_k: int = 5,
    ):
        # 相变阈值：局部密度超过此值才形成液滴（类比临界浓度）
        self.density_threshold = density_threshold
        # 表面张力：液滴融合的能量屏障（边界亲和力需超过此值）
        self.surface_tension = surface_tension
        # 液滴大小约束：防止单液滴过大（避免"老化"固化）
        self.min_droplet_size = min_droplet_size
        self.max_droplet_size = max_droplet_size
        # 局部密度计算时考虑的邻居数（类比多价相互作用域数量）
        self.neighbor_k = neighbor_k
        # 当前液滴集合
        self.droplets: list[KnowledgeDroplet] = []

    def _pairwise_similarity(self, embeddings: list[Vec]) -> Matrix:
        """计算概念间余弦相似度（类比蛋白质多价相互作用强度）"""
        n = len(embeddings)
        sim = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                s = cosine(embeddings[i], embeddings[j])
                sim[i][j] = s
                sim[j][i] = s
        return sim

    def _local_density(self, sim: Matrix) -> list[float]:
        """每个概念的局部密度 = top-k 邻居相似度均值（类比局部浓度）"""
        n = len(sim)
        k = min(self.neighbor_k, n - 1)
        densities = []
        for i in range(n):
            neighbors = sorted(sim[i], reverse=True)[:k]
            densities.append(sum(neighbors) / max(k, 1))
        return densities

    def organize(self, embeddings: list[Vec]) -> list[KnowledgeDroplet]:
        """相分离主过程：将嵌入组织成知识液滴。"""
        n = len(embeddings)
        if n < self.min_droplet_size:
            self.droplets = []
            return self.droplets

        sim = self._pairwise_similarity(embeddings)
        density = self._local_density(sim)

        # 按密度降序处理：从最高密度节点开始成核（类比液滴的相变成核）
        order = sorted(range(n), key=lambda i: -density[i])
        assigned = [False] * n
        droplets: list[KnowledgeDroplet] = []

        for i in order:
            if assigned[i] or density[i] < self.density_threshold:
                continue

            # 成核：收集与 i 强相互作用的未分配节点作为核心
            core = [i]
            assigned[i] = True
            for j in range(n):
                if assigned[j]:
                    continue
                if sim[i][j] > self.density_threshold * 0.85:
                    core.append(j)
                    assigned[j] = True
                    if len(core) >= self.max_droplet_size:
                        break

            if len(core) < self.min_droplet_size:
                # 未达到最小液滴规模，回滚分配
                for c in core:
                    assigned[c] = False
                continue

            # 边界：与液滴核心有中等亲和力的未分配节点
            boundary = []
            for j in range(n):
                if assigned[j]:
                    continue
                affinity = max(sim[c][j] for c in core)
                if affinity > self.density_threshold * 0.6:
                    boundary.append(j)
                    assigned[j] = True
                    if len(core) + len(boundary) >= self.max_droplet_size:
                        break

            centroid = vec_mean([embeddings[idx] for idx in core])
            droplets.append(KnowledgeDroplet(len(droplets), core, boundary, centroid))

        self.droplets = droplets
        self._merge_pass(embeddings)
        return self.droplets

    def _boundary_affinity(self, d1: KnowledgeDroplet, d2: KnowledgeDroplet, embeddings: list[Vec]) -> float:
        """两液滴边界概念的平均亲和力（类比液滴接触面张力）"""
        b1 = d1.boundary or d1.core
        b2 = d2.boundary or d2.core
        scores = [cosine(embeddings[i], embeddings[j]) for i in b1 for j in b2]
        return sum(scores) / len(scores) if scores else 0.0

    def _merge_pass(self, embeddings: list[Vec]):
        """液滴融合：边界亲和力超过表面张力时合并（类比液滴融合）"""
        changed = True
        while changed:
            changed = False
            merged = [False] * len(self.droplets)
            new_droplets: list[KnowledgeDroplet] = []

            for i, d1 in enumerate(self.droplets):
                if merged[i]:
                    continue
                for j in range(i + 1, len(self.droplets)):
                    if merged[j]:
                        continue
                    d2 = self.droplets[j]
                    if d1.size + d2.size > self.max_droplet_size:
                        continue
                    if self._boundary_affinity(d1, d2, embeddings) > self.surface_tension:
                        # 合并：核心并核心，边界去重后相加
                        new_core = d1.core + d2.core
                        new_boundary = list(set(d1.boundary + d2.boundary) - set(new_core))
                        new_centroid = vec_mean([embeddings[idx] for idx in new_core])
                        new_droplets.append(KnowledgeDroplet(
                            len(new_droplets), new_core, new_boundary, new_centroid
                        ))
                        merged[i] = merged[j] = True
                        changed = True
                        break
                if not merged[i]:
                    new_droplets.append(KnowledgeDroplet(
                        len(new_droplets), d1.core, d1.boundary, d1.centroid
                    ))
                    merged[i] = True

            self.droplets = new_droplets

    # ─── 液滴内注意力 ─────────────────────────────────────────────────────

    def droplet_attention(
        self,
        query: list[Vec],
        key: list[Vec],
        value: list[Vec],
        droplet: KnowledgeDroplet,
        amplification: float = 1.5,
    ) -> dict[int, Vec]:
        """液滴内注意力：复杂度 O(m²)，浓缩放大增强液滴内交互。

        amplification > 1 对应液滴内分子浓度提升带来的反应速率增益。
        """
        idx = droplet.members
        m = len(idx)
        dim = len(query[0])
        scale = math.sqrt(dim) / amplification

        # 计算 attention scores（液滴内 m × m）
        scores: Matrix = [[dot(query[idx[i]], key[idx[j]]) / scale for j in range(m)] for i in range(m)]

        # softmax（数值稳定）
        outputs: dict[int, Vec] = {}
        for i in range(m):
            row_max = max(scores[i])
            exps = [math.exp(s - row_max) for s in scores[i]]
            z = sum(exps)
            weights = [e / z for e in exps]
            # 加权求和
            out = [sum(weights[j] * value[idx[j]][d] for j in range(m)) for d in range(dim)]
            outputs[idx[i]] = out
        return outputs

    # ─── 查询激活 ─────────────────────────────────────────────────────────

    def query(self, query_embedding: Vec, top_k: int = 3) -> list[tuple[KnowledgeDroplet, float]]:
        """查询激活：根据查询嵌入激活最相关的液滴（类比信号激活无膜细胞器）"""
        scored = [(d, cosine(query_embedding, d.centroid)) for d in self.droplets]
        scored.sort(key=lambda x: -x[1])
        return scored[:top_k]

    # ─── 统计 ─────────────────────────────────────────────────────────────

    def stats(self) -> dict:
        if not self.droplets:
            return {"num_droplets": 0, "coverage": 0}
        sizes = [d.size for d in self.droplets]
        return {
            "num_droplets": len(self.droplets),
            "avg_size": sum(sizes) / len(sizes),
            "max_size": max(sizes),
            "min_size": min(sizes),
            "coverage": sum(sizes),
        }
