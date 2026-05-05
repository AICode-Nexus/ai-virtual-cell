"""P0-2 创新原型：免疫检查点式对齐 (Immune Checkpoint Alignment)

生物学基础：
    PD-1 / CTLA-4 免疫检查点通过抑制信号动态平衡免疫反应，
    避免 T 细胞过度激活造成自身损伤。

AI 对应：
    当前 AI 安全系统缺乏动态平衡机制，常表现为过度拒绝 (over-refusal)。
    本模块模拟免疫检查点：根据上下文（用户可信度、请求风险、对话记忆）
    动态调节安全阈值，在安全性与有用性之间取得平衡。
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# 确保所在目录存在（便于作为脚本独立运行时使用）
os.makedirs(os.path.dirname(__file__), exist_ok=True)


@dataclass
class SafetyContext:
    """安全上下文：对应免疫系统的抗原识别环境。"""

    user_trust: float          # 0-1，用户可信度  —— 类比 MHC 呈递（自我识别）
    request_risk: float        # 0-1，请求风险度  —— 类比抗原危险信号
    conversation_depth: int    # 对话轮数        —— 类比免疫记忆（记忆 B/T 细胞）


class ImmuneCheckpointAligner:
    """免疫检查点式对齐器。

    核心思想：
        T 细胞激活强度 = 激活信号 - 抑制信号 (PD-1/CTLA-4)
        类比：AI 拒绝倾向   = 风险信号 - 抑制信号（信任/记忆带来的容忍）
    """

    def __init__(self, base_threshold: float = 0.5) -> None:
        # 基础安全阈值：无上下文信息时的默认拒绝门槛
        self.base_threshold = base_threshold

    # ------------------------------------------------------------------
    # 抑制信号：高信任 + 低风险 + 长对话记忆 → 强抑制（允许更多）
    # ------------------------------------------------------------------
    def compute_inhibitory_signal(self, context: SafetyContext) -> float:
        """计算抑制信号强度（0-1），类比 PD-1/CTLA-4 对 T 细胞的抑制。"""
        trust_term = context.user_trust                 # MHC：自我识别越强，越抑制攻击
        risk_term = 1.0 - context.request_risk          # 风险越低，越允许
        # 免疫记忆：对话越长（上限 10 轮），抑制越强，避免反复误判
        memory_term = min(context.conversation_depth, 10) / 10.0

        # 加权融合（信任 0.5 / 低风险 0.3 / 记忆 0.2）
        signal = 0.5 * trust_term + 0.3 * risk_term + 0.2 * memory_term
        return max(0.0, min(1.0, signal))

    # ------------------------------------------------------------------
    # 动态安全阈值：基础阈值随抑制信号上移（更宽容）
    # ------------------------------------------------------------------
    def get_dynamic_threshold(self, context: SafetyContext) -> float:
        """动态安全阈值 = 基础阈值 + 抑制信号调节。"""
        inhibition = self.compute_inhibitory_signal(context)
        # 抑制信号最高可将阈值上调 0.4，表示更宽容
        threshold = self.base_threshold + 0.4 * (inhibition - 0.5)
        return max(0.1, min(0.95, threshold))

    # ------------------------------------------------------------------
    # 拒绝决策
    # ------------------------------------------------------------------
    def should_refuse(self, harm_score: float, context: SafetyContext) -> bool:
        """harm_score 超过动态阈值则拒绝（类比 T 细胞是否激活攻击）。"""
        return harm_score >= self.get_dynamic_threshold(context)

    # ------------------------------------------------------------------
    # 响应模式：strict / balanced / permissive
    # ------------------------------------------------------------------
    def get_response_mode(self, context: SafetyContext) -> str:
        threshold = self.get_dynamic_threshold(context)
        if threshold < 0.4:
            return "strict"      # 高警戒：类比急性炎症反应
        if threshold < 0.65:
            return "balanced"    # 常态平衡：类比稳态免疫
        return "permissive"      # 宽容：类比免疫耐受


# ----------------------------------------------------------------------
# 演示
# ----------------------------------------------------------------------
def demo() -> None:
    aligner = ImmuneCheckpointAligner(base_threshold=0.5)

    scenarios = {
        "新用户 + 高风险请求":       SafetyContext(user_trust=0.1, request_risk=0.9, conversation_depth=0),
        "老用户 + 低风险闲聊":       SafetyContext(user_trust=0.9, request_risk=0.1, conversation_depth=8),
        "中等信任 + 中等风险":       SafetyContext(user_trust=0.5, request_risk=0.5, conversation_depth=3),
        "高信任 + 高风险（可疑）":   SafetyContext(user_trust=0.9, request_risk=0.85, conversation_depth=5),
    }

    print(f"{'场景':<28}{'抑制信号':>10}{'动态阈值':>10}{'模式':>14}")
    print("-" * 64)
    for name, ctx in scenarios.items():
        inh = aligner.compute_inhibitory_signal(ctx)
        thr = aligner.get_dynamic_threshold(ctx)
        mode = aligner.get_response_mode(ctx)
        print(f"{name:<28}{inh:>10.3f}{thr:>10.3f}{mode:>14}")

    print()
    sample_harm = 0.6
    print(f"示例：harm_score = {sample_harm} 时是否拒绝：")
    for name, ctx in scenarios.items():
        refuse = aligner.should_refuse(sample_harm, ctx)
        print(f"  - {name}: {'拒绝' if refuse else '允许'}")


if __name__ == "__main__":
    demo()
