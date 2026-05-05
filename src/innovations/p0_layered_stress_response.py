"""P0-3 创新原型：分层应激响应系统 (Layered Stress Response System)

生物学基础：
    - 未折叠蛋白响应 (UPR) 三臂机制：IRE1 / PERK / ATF6
    - 热休克蛋白 (HSP) 辅助折叠
    - 细胞自噬 (Autophagy) 清理受损组件

核心思想：根据应激严重程度分级响应
    - 轻度 (MILD)    → 降级服务     ~ IRE1  轻量剪接修复
    - 中度 (MODERATE)→ 检查点回滚   ~ PERK  暂停翻译/回退
    - 重度 (SEVERE)  → 触发重训练   ~ ATF6  大规模基因表达重塑
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List

# 确保 innovations 目录存在（便于作为脚本使用时自动创建）
os.makedirs(os.path.dirname(__file__), exist_ok=True)


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------
@dataclass
class StressMetrics:
    """应激指标（类比细胞内稳态失衡信号）"""
    error_rate: float              # 0-1，错误率 ~ 蛋白质错误折叠率
    latency_multiplier: float      # 延迟倍数 ~ 代谢负荷
    memory_pressure: float         # 0-1，内存压力 ~ 内质网 (ER) 应激
    timestamp: float = field(default_factory=time.time)


class StressLevel(Enum):
    """应激级别（对应 UPR 三臂）"""
    MILD = "mild"          # IRE1: 局部剪接修复
    MODERATE = "moderate"  # PERK: 暂停翻译，回退到稳定态
    SEVERE = "severe"      # ATF6: 全局基因表达重塑（重训练）


@dataclass
class ResponseAction:
    """响应动作"""
    level: StressLevel
    strategy: str           # 'degrade_service' / 'checkpoint_rollback' / 'trigger_retrain'
    description: str
    urgency: float          # 0-1，紧急程度


# ---------------------------------------------------------------------------
# 分层应激响应器
# ---------------------------------------------------------------------------
class LayeredStressResponder:
    """分层应激响应系统：根据综合应激评分决定响应策略。"""

    # 阈值（类比 UPR 激活所需的错误折叠蛋白积累量）
    MILD_THRESHOLD: float = 0.20
    MODERATE_THRESHOLD: float = 0.45
    SEVERE_THRESHOLD: float = 0.75

    # 综合评分权重
    W_ERROR = 0.5
    W_LATENCY = 0.25
    W_MEMORY = 0.25

    def get_stress_score(self, metrics: StressMetrics) -> float:
        """综合应激评分 (0-1)：错误率权重最高，其次延迟与内存压力。"""
        # 将延迟倍数归一化：1x = 无应激，5x 及以上 = 满载
        latency_norm = max(0.0, min(1.0, (metrics.latency_multiplier - 1.0) / 4.0))
        score = (
            self.W_ERROR * metrics.error_rate
            + self.W_LATENCY * latency_norm
            + self.W_MEMORY * metrics.memory_pressure
        )
        return max(0.0, min(1.0, score))

    def classify_stress(self, metrics: StressMetrics) -> StressLevel:
        """UPR 三臂类比分级：IRE1 / PERK / ATF6 对应三个严重级别。"""
        score = self.get_stress_score(metrics)
        if score >= self.MODERATE_THRESHOLD:
            # 超过 SEVERE_THRESHOLD 时进入 ATF6 路径
            if score >= self.SEVERE_THRESHOLD:
                return StressLevel.SEVERE
            return StressLevel.MODERATE
        return StressLevel.MILD

    def get_response(self, metrics: StressMetrics) -> ResponseAction:
        """根据应激级别生成响应动作。"""
        level = self.classify_stress(metrics)
        score = self.get_stress_score(metrics)

        if level is StressLevel.SEVERE:
            return ResponseAction(
                level=level,
                strategy="trigger_retrain",
                description="重度应激：触发模型重训练（类比 ATF6 驱动的基因表达重塑）",
                urgency=score,
            )
        if level is StressLevel.MODERATE:
            return ResponseAction(
                level=level,
                strategy="checkpoint_rollback",
                description="中度应激：回滚到最近稳定检查点（类比 PERK 暂停翻译）",
                urgency=score,
            )
        return ResponseAction(
            level=level,
            strategy="degrade_service",
            description="轻度应激：启用降级服务（类比 IRE1 局部剪接修复）",
            urgency=score,
        )

    def monitor_and_respond(self, metrics_stream: List[StressMetrics]) -> List[ResponseAction]:
        """批量处理一系列指标，返回响应序列。"""
        return [self.get_response(m) for m in metrics_stream]


# ---------------------------------------------------------------------------
# 演示
# ---------------------------------------------------------------------------
def demo() -> None:
    """模拟一系列故障场景并展示分层响应。"""
    responder = LayeredStressResponder()

    # 模拟场景：正常 → 轻度抖动 → 中度退化 → 重度崩溃 → 恢复
    scenarios = [
        ("稳态运行",      StressMetrics(error_rate=0.02, latency_multiplier=1.1, memory_pressure=0.10)),
        ("轻度抖动",      StressMetrics(error_rate=0.15, latency_multiplier=1.8, memory_pressure=0.30)),
        ("中度退化",      StressMetrics(error_rate=0.50, latency_multiplier=3.0, memory_pressure=0.60)),
        ("重度崩溃",      StressMetrics(error_rate=0.85, latency_multiplier=4.8, memory_pressure=0.90)),
        ("缓慢恢复",      StressMetrics(error_rate=0.20, latency_multiplier=1.5, memory_pressure=0.25)),
    ]

    print("=" * 72)
    print("分层应激响应系统 演示 (UPR 三臂类比)")
    print("=" * 72)
    for name, m in scenarios:
        action = responder.get_response(m)
        score = responder.get_stress_score(m)
        print(
            f"[{name:<8}] score={score:.2f}  level={action.level.value:<8}  "
            f"strategy={action.strategy:<20}  urgency={action.urgency:.2f}"
        )
        print(f"           → {action.description}")
    print("=" * 72)

    # 批处理接口演示
    actions = responder.monitor_and_respond([m for _, m in scenarios])
    counts = {lvl: 0 for lvl in StressLevel}
    for a in actions:
        counts[a.level] += 1
    print("响应汇总：", {k.value: v for k, v in counts.items()})


if __name__ == "__main__":
    demo()
