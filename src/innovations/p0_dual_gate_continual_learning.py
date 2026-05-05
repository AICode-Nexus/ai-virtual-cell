"""
P0-1 创新原型：双重门控持续学习 (Dual-Gate Continual Learning)

生物学基础：突触标记与捕获 (Synaptic Tagging and Capture, STC)
 - 局部标记 (local tag)：单个突触在强活动下设置短暂标记
 - 全局捕获信号 (global PRP)：细胞核合成的可塑性相关蛋白广播至全细胞
 - 只有"被标记 AND 捕获到 PRP"的突触才发生长期巩固 (LTP)

AI 缺口：EWC/SI 仅依赖全局 Fisher 信息，缺乏局部-全局协同门控
→ 保护范围过广，新任务学习受阻。

纯 Python 实现，参数用 list[float] 表示。
"""
from __future__ import annotations

# 参数类型别名：list[float] 模拟扁平化的权重向量
Params = list[float]


class DualGateContinualLearner:
    """双重门控持续学习器：local tag × global PRP → consolidation。"""

    def __init__(self, local_threshold: float = 0.1, global_threshold: float = 0.5):
        # 局部标记阈值：对应突触局部活动强度门限
        self.local_threshold = local_threshold
        # 全局信号阈值：对应 PRP 合成/释放的细胞级门限
        self.global_threshold = global_threshold
        # 局部标记：参数名 -> 标记强度列表 (类比 synaptic tag)
        self.tags: dict[str, Params] = {}
        # 巩固权重：参数名 -> 保护权重列表 (类比 LTP 后的突触权重保护)
        self.consolidation_weights: dict[str, Params] = {}

    def tag_parameters(self, gradients: dict[str, Params]) -> dict[str, Params]:
        """基于梯度幅度设置局部标记 (synaptic tagging)。
        梯度大 = 该参数对当前任务高度活跃 → 打上局部标记。
        """
        for name, grad in gradients.items():
            # 软标记：超过阈值的幅度作为标记强度，低于阈值置 0
            self.tags[name] = [abs(g) if abs(g) >= self.local_threshold else 0.0 for g in grad]
        return self.tags

    def compute_consolidation_weights(self, global_signal: float) -> dict[str, Params]:
        """双重门控：只有 local tag 与 global PRP 信号同时激活时才保护参数。
        global_signal 类比任务重要性触发的 PRP 合成强度。
        """
        gate_open = global_signal >= self.global_threshold
        for name, tag in self.tags.items():
            # AND 门：全局门开启时 consolidation = tag × global_signal，否则为 0
            self.consolidation_weights[name] = [t * global_signal for t in tag] if gate_open else [0.0] * len(tag)
        return self.consolidation_weights

    def ewc_penalty(
        self,
        current_params: dict[str, Params],
        reference_params: dict[str, Params],
    ) -> float:
        """双重门控版 EWC 正则化损失：L = Σ w_i * (θ_i - θ*_i)^2。
        w_i 为双重门控后的巩固权重（而非全局 Fisher）。
        """
        total = 0.0
        for name, theta in current_params.items():
            if name not in self.consolidation_weights:
                continue
            ref = reference_params[name]
            w = self.consolidation_weights[name]
            total += sum(wi * (ti - ri) ** 2 for wi, ti, ri in zip(w, theta, ref))
        return total
