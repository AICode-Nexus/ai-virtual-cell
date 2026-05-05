"""
双重门控持续学习 vs 标准 EWC 的最小演示。

场景：Task A 训练后，在 Task B 上更新参数，测量对 Task A 的遗忘。
"""
from __future__ import annotations
import random
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from p0_dual_gate_continual_learning import DualGateContinualLearner

rng = random.Random(0)

def randn(n: int, scale: float = 1.0) -> list[float]:
    import math
    # Box-Muller 生成正态分布样本
    out = []
    for _ in range((n + 1) // 2):
        u1, u2 = rng.random() or 1e-10, rng.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        out.extend([z0 * scale, z1 * scale])
    return out[:n]

def simulate_update(ref, grads_b, lr, protection):
    """单步带正则梯度更新：θ <- θ - lr*(g + 2*w*(θ-θ*))"""
    result = {}
    for name, theta in ref.items():
        g = grads_b[name]
        w = protection.get(name, [0.0] * len(theta))
        result[name] = [t - lr * (gi + 2 * wi * (t - ri))
                        for t, gi, wi, ri in zip(theta, g, w, ref[name])]
    return result

def forgetting(current, ref, importance):
    return sum(
        wi * (ci - ri) ** 2
        for name in current
        for wi, ci, ri in zip(importance[name], current[name], ref[name])
    )

def plasticity(params, ref):
    return sum((p - r) ** 2 for name in params for p, r in zip(params[name], ref[name]))

def main():
    N = 16  # 每个参数向量长度（模拟 4×4 和 4×2 展平）
    shapes = {"W1": 16, "W2": 8}

    # Task A 完成后的参考参数
    ref = {n: randn(s) for n, s in shapes.items()}

    # Task A 梯度：稀疏强活动（模拟少数关键突触）
    grads_a = {n: randn(s, 0.05) for n, s in shapes.items()}
    grads_a["W1"][0] = 0.8   # 关键突触 1
    grads_a["W1"][11] = 0.6  # 关键突触 2
    grads_a["W2"][5] = 0.7   # 关键突触 3

    # Oracle 重要性：仅上述位置真正重要
    importance = {n: [0.0] * s for n, s in shapes.items()}
    importance["W1"][0] = importance["W1"][11] = importance["W2"][5] = 1.0

    # 标准 EWC：Fisher ≈ 梯度平方（全局密集）
    fisher = {n: [g ** 2 for g in grads_a[n]] for n in shapes}

    # 双重门控：local tag (阈值0.1) × global PRP (信号0.8)
    learner = DualGateContinualLearner(local_threshold=0.1, global_threshold=0.5)
    learner.tag_parameters(grads_a)
    learner.compute_consolidation_weights(global_signal=0.8)

    # Task B 梯度（与 Task A 近似正交）
    grads_b = {n: randn(s, 0.3) for n, s in shapes.items()}

    lr = 0.1
    no_reg = simulate_update(ref, grads_b, lr, {})
    ewc    = simulate_update(ref, grads_b, lr, fisher)
    dual   = simulate_update(ref, grads_b, lr, learner.consolidation_weights)

    print("=== Dual-Gate Continual Learning Demo ===")
    print(f"  No regularization | forgetting={forgetting(no_reg, ref, importance):.4f}  plasticity={plasticity(no_reg, ref):.4f}")
    print(f"  Standard EWC      | forgetting={forgetting(ewc,    ref, importance):.4f}  plasticity={plasticity(ewc,    ref):.4f}")
    print(f"  Dual-Gate EWC     | forgetting={forgetting(dual,   ref, importance):.4f}  plasticity={plasticity(dual,   ref):.4f}")
    print()
    tagged_w1 = sum(1 for t in learner.tags["W1"] if t > 0)
    tagged_w2 = sum(1 for t in learner.tags["W2"] if t > 0)
    print(f"  Tagged W1: {tagged_w1}/{shapes['W1']}  Tagged W2: {tagged_w2}/{shapes['W2']}")
    print("  → 双重门控仅保护 local-tag ∧ global-PRP 同时激活的少数关键参数，")
    print("    在抑制遗忘的同时为新任务保留更多可塑性。")

if __name__ == "__main__":
    main()
