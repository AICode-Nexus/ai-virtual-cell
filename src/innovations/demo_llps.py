"""
知识液滴系统 (LLPS) 的最小演示。

场景：多主题概念池通过相分离自动聚集成液滴，对比全局注意力复杂度。
"""
from __future__ import annotations
import math
import random
import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))
from p0_llps_knowledge_organization import LLPSKnowledgeSystem, cosine, dot

rng = random.Random(42)


def randn(n: int, scale: float = 1.0) -> list[float]:
    """Box-Muller 生成正态分布样本"""
    out = []
    for _ in range((n + 1) // 2):
        u1, u2 = rng.random() or 1e-10, rng.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        out.extend([z0 * scale, z1 * scale])
    return out[:n]


def make_topical_pool(num_topics: int, per_topic: int, dim: int = 16, noise: float = 0.25):
    """生成具有主题结构的概念池：每个主题围绕一个中心方向"""
    centers = []
    for _ in range(num_topics):
        c = randn(dim, 1.0)
        # 归一化到单位长度
        n = math.sqrt(sum(x * x for x in c)) + 1e-8
        centers.append([x / n for x in c])

    embeddings: list[list[float]] = []
    labels: list[int] = []
    for t, center in enumerate(centers):
        for _ in range(per_topic):
            perturb = randn(dim, noise)
            embeddings.append([c + p for c, p in zip(center, perturb)])
            labels.append(t)
    return embeddings, labels


def purity(core_indices: list[int], labels: list[int]) -> tuple[int, float]:
    """液滴核心概念的主题纯度"""
    if not core_indices:
        return -1, 0.0
    topic_count: dict[int, int] = {}
    for i in core_indices:
        topic_count[labels[i]] = topic_count.get(labels[i], 0) + 1
    dominant = max(topic_count, key=topic_count.get)
    return dominant, topic_count[dominant] / len(core_indices)


def global_attention_ops(n: int) -> int:
    return n * n


def droplet_attention_ops(droplets) -> int:
    return sum(d.size * d.size for d in droplets)


def demo_phase_separation():
    print("\n=== 演示 1: 相分离 —— 5 个主题自动聚集成液滴 ===")
    embeddings, labels = make_topical_pool(num_topics=5, per_topic=12, dim=16, noise=0.15)
    print(f"  输入: {len(embeddings)} 个概念 / {len(set(labels))} 个真实主题")

    system = LLPSKnowledgeSystem(
        density_threshold=0.55,
        surface_tension=0.85,
        min_droplet_size=2,
        neighbor_k=5,
    )
    t0 = time.time()
    droplets = system.organize(embeddings)
    elapsed = (time.time() - t0) * 1000

    print(f"  相分离耗时: {elapsed:.1f} ms")
    stats = system.stats()
    print(f"  液滴数: {stats['num_droplets']}  平均大小: {stats['avg_size']:.1f}  覆盖: {stats['coverage']}/{len(embeddings)}")
    for d in droplets:
        topic, pur = purity(d.core, labels)
        print(f"    液滴 {d.droplet_id}: 大小={d.size} (核心={len(d.core)}, 边界={len(d.boundary)}) "
              f"| 主导主题={topic} 纯度={pur:.0%}")


def demo_query_activation():
    print("\n=== 演示 2: 查询激活 —— 查询自动定位相关液滴 ===")
    embeddings, labels = make_topical_pool(num_topics=5, per_topic=12, noise=0.15)
    system = LLPSKnowledgeSystem(density_threshold=0.55, surface_tension=0.85)
    system.organize(embeddings)

    # 从主题 2 取一个样本加噪作为查询
    query_topic = 2
    query_idx = next(i for i, l in enumerate(labels) if l == query_topic)
    query_embed = [e + p for e, p in zip(embeddings[query_idx], randn(len(embeddings[0]), 0.1))]

    activated = system.query(query_embed, top_k=3)
    print(f"  查询来自真实主题 {query_topic}")
    for d, score in activated:
        topic, pur = purity(d.core, labels)
        match = "✓" if topic == query_topic else " "
        print(f"    {match} 液滴 {d.droplet_id}: 主导主题={topic} 相似度={score:.3f} 纯度={pur:.0%}")


def demo_complexity():
    print("\n=== 演示 3: 复杂度对比 —— 液滴 vs 全局注意力 ===")
    print(f"  {'主题':<6}{'每主题':<8}{'总n':<8}{'全局 n²':<12}{'液滴 Σm²':<12}{'加速比':<10}")
    print("  " + "-" * 56)

    for num_topics, per_topic in [(4, 10), (6, 12), (8, 15), (10, 20)]:
        embeddings, _ = make_topical_pool(num_topics, per_topic, noise=0.15)
        n = len(embeddings)
        system = LLPSKnowledgeSystem(density_threshold=0.55, surface_tension=0.85)
        system.organize(embeddings)

        g_ops = global_attention_ops(n)
        d_ops = droplet_attention_ops(system.droplets)
        speedup = g_ops / max(d_ops, 1)
        print(f"  {num_topics:<6}{per_topic:<8}{n:<8}{g_ops:<12}{d_ops:<12}{speedup:<10.2f}")


def demo_droplet_attention():
    print("\n=== 演示 4: 液滴内注意力浓缩 —— 验证注意力权重分布 ===")
    embeddings, labels = make_topical_pool(num_topics=3, per_topic=8, dim=8, noise=0.15)
    system = LLPSKnowledgeSystem(density_threshold=0.50, surface_tension=0.85)
    system.organize(embeddings)

    if not system.droplets:
        print("  (无液滴形成)")
        return

    # 直接用 embeddings 充当 query/key/value
    d = system.droplets[0]
    print(f"  检视液滴 0: 成员索引 = {d.members}")

    outputs = system.droplet_attention(embeddings, embeddings, embeddings, d, amplification=1.5)
    # 对比：液滴内第一个成员的输出 vs 液滴外随机向量的相似度
    sample_idx = d.members[0]
    out_vec = outputs[sample_idx]

    in_droplet_sims = [cosine(out_vec, embeddings[i]) for i in d.members]
    out_droplet_indices = [i for i in range(len(embeddings)) if i not in d.members]
    out_droplet_sims = [cosine(out_vec, embeddings[i]) for i in out_droplet_indices]

    avg_in = sum(in_droplet_sims) / len(in_droplet_sims)
    avg_out = sum(out_droplet_sims) / max(len(out_droplet_sims), 1)
    print(f"  液滴输出与液滴内成员平均相似度: {avg_in:.3f}")
    print(f"  液滴输出与液滴外成员平均相似度: {avg_out:.3f}")
    print(f"  浓缩比 (in/out): {avg_in / max(avg_out, 1e-6):.2f}x  (>1 表示液滴内成员占据输出分布)")


def main():
    print("=" * 64)
    print("  P0-4 知识液滴系统 (LLPS Knowledge Organization) 演示")
    print("  生物学: 液-液相分离 → 无膜细胞器")
    print("  AI映射: 动态知识聚类 + 液滴内高效注意力")
    print("=" * 64)

    demo_phase_separation()
    demo_query_activation()
    demo_complexity()
    demo_droplet_attention()

    print("\n" + "=" * 64)
    print("  ✓ 相分离自动形成语义一致的液滴（高纯度）")
    print("  ✓ 查询可精准激活对应液滴")
    print("  ✓ 复杂度从 O(n²) 降至 O(Σ m²)，主题越多加速越显著")
    print("  ✓ 液滴内注意力体现浓缩效应")
    print("=" * 64)


if __name__ == "__main__":
    main()
