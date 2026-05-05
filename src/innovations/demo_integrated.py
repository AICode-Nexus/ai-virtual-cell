#!/usr/bin/env python3
"""
AI Virtual Cell - P0创新集成演示
展示三个P0创新如何协同工作构建鲁棒的持续学习系统
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from p0_dual_gate_continual_learning import DualGateContinualLearner
from p0_immune_checkpoint_alignment import ImmuneCheckpointAligner, SafetyContext
from p0_layered_stress_response import LayeredStressResponder, StressMetrics, StressLevel
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class SystemState:
    """AI系统状态（类比细胞状态）"""
    task_id: int
    performance: float  # 0-1
    safety_score: float  # 0-1
    stress_level: StressLevel


class IntegratedAIVirtualCell:
    """
    集成AI虚拟细胞：结合三个P0创新

    生物类比：
    - 双重门控 = 突触可塑性（学习与记忆）
    - 免疫检查点 = 免疫系统（安全与平衡）
    - 应激响应 = 应激响应系统（容错与恢复）
    """

    def __init__(self):
        self.learner = DualGateContinualLearner(
            local_threshold=0.1,
            global_threshold=0.5
        )
        self.aligner = ImmuneCheckpointAligner(base_threshold=0.4)
        self.responder = LayeredStressResponder()

        self.current_task = 0
        self.parameters = {'w1': [0.5] * 10, 'w2': [0.3] * 5}

    def learn_task(self, task_id: int, gradients: Dict[str, List[float]],
                   task_importance: float) -> SystemState:
        """
        学习新任务（持续学习场景）

        Args:
            task_id: 任务ID
            gradients: 参数梯度
            task_importance: 任务重要性（全局PRP信号）

        Returns:
            系统状态
        """
        # P0-1: 双重门控持续学习
        self.learner.tag_parameters(gradients)
        consolidation = self.learner.compute_consolidation_weights(task_importance)

        # 模拟学习（简化）
        for param_name, grad in gradients.items():
            if param_name in self.parameters:
                protection_weights = consolidation.get(param_name, [0.0] * len(grad))
                for i in range(len(grad)):
                    # 受保护参数更新幅度更小
                    protection = protection_weights[i] if i < len(protection_weights) else 0.0
                    learning_rate = 0.01 * (1.0 - min(protection, 1.0) * 0.8)
                    self.parameters[param_name][i] -= learning_rate * grad[i]

        # 计算性能（简化）
        performance = 0.85 + task_importance * 0.1

        # 评估应激水平
        stress = StressMetrics(
            error_rate=1.0 - performance,
            latency_multiplier=1.0 + (1.0 - performance) * 2.0,
            memory_pressure=len(consolidation) / 20.0,
            timestamp=float(task_id)
        )
        stress_level = self.responder.classify_stress(stress)

        return SystemState(
            task_id=task_id,
            performance=performance,
            safety_score=0.9,
            stress_level=stress_level
        )

    def handle_request(self, request: str, user_trust: float,
                       request_risk: float) -> tuple[bool, str]:
        """
        处理用户请求（安全对齐场景）

        Args:
            request: 用户请求
            user_trust: 用户可信度 (0-1)
            request_risk: 请求风险度 (0-1)

        Returns:
            (是否允许, 响应模式)
        """
        # P0-2: 免疫检查点式对齐
        context = SafetyContext(
            user_trust=user_trust,
            request_risk=request_risk,
            conversation_depth=5
        )

        # 模拟危害评分
        harm_score = request_risk * 0.7

        should_refuse = self.aligner.should_refuse(harm_score, context)
        mode = self.aligner.get_response_mode(context)

        return (not should_refuse, mode)

    def handle_failure(self, error_rate: float, latency_mult: float,
                       memory_pressure: float) -> str:
        """
        处理系统故障（容错场景）

        Args:
            error_rate: 错误率 (0-1)
            latency_mult: 延迟倍数
            memory_pressure: 内存压力 (0-1)

        Returns:
            响应策略
        """
        # P0-3: 分层应激响应
        stress = StressMetrics(
            error_rate=error_rate,
            latency_multiplier=latency_mult,
            memory_pressure=memory_pressure,
            timestamp=0.0
        )

        response = self.responder.get_response(stress)
        return response.strategy


def demo():
    """集成演示：展示三个P0创新协同工作"""
    print("=" * 70)
    print("AI Virtual Cell - P0创新集成演示")
    print("=" * 70)
    print()

    cell = IntegratedAIVirtualCell()

    # 场景1：持续学习（双重门控）
    print("【场景1：持续学习 - 双重门控机制】")
    print("-" * 70)

    tasks = [
        (1, {'w1': [0.2] * 10, 'w2': [0.1] * 5}, 0.8, "高重要性任务"),
        (2, {'w1': [0.05] * 10, 'w2': [0.15] * 5}, 0.3, "低重要性任务"),
        (3, {'w1': [0.18] * 10, 'w2': [0.02] * 5}, 0.9, "关键任务"),
    ]

    for task_id, grads, importance, desc in tasks:
        state = cell.learn_task(task_id, grads, importance)
        print(f"Task {task_id} ({desc})")
        print(f"  重要性={importance:.1f} | 性能={state.performance:.3f} | "
              f"应激={state.stress_level.name}")

    print()

    # 场景2：安全对齐（免疫检查点）
    print("【场景2：安全对齐 - 免疫检查点机制】")
    print("-" * 70)

    requests = [
        ("正常查询", 0.9, 0.1),
        ("边缘请求", 0.5, 0.5),
        ("可疑请求", 0.2, 0.8),
        ("老用户灰色地带", 0.95, 0.6),
    ]

    for desc, trust, risk in requests:
        allowed, mode = cell.handle_request(desc, trust, risk)
        status = "✓ 允许" if allowed else "✗ 拒绝"
        print(f"{desc:12s} | 信任={trust:.1f} 风险={risk:.1f} | "
              f"{status:6s} | 模式={mode}")

    print()

    # 场景3：容错恢复（分层应激响应）
    print("【场景3：容错恢复 - 分层应激响应机制】")
    print("-" * 70)

    failures = [
        (0.05, 1.2, 0.1, "轻微抖动"),
        (0.15, 2.0, 0.3, "性能下降"),
        (0.35, 3.5, 0.6, "中度故障"),
        (0.70, 8.0, 0.9, "严重崩溃"),
    ]

    for err, lat, mem, desc in failures:
        strategy = cell.handle_failure(err, lat, mem)
        print(f"{desc:12s} | 错误={err:.2f} 延迟={lat:.1f}x 内存={mem:.1f} | "
              f"策略={strategy}")

    print()

    # 综合场景：三个机制协同工作
    print("【场景4：综合协同 - 三机制联动】")
    print("-" * 70)
    print("模拟：系统在学习新任务时遇到故障，需要安全对齐决策")
    print()

    # 学习高风险任务
    print("1. 学习高风险任务（双重门控）")
    state = cell.learn_task(4, {'w1': [0.25] * 10, 'w2': [0.2] * 5}, 0.95)
    print(f"   → 性能={state.performance:.3f}, 应激={state.stress_level.name}")

    # 检测到性能下降，触发应激响应
    if state.performance < 0.9:
        print("2. 检测到性能下降（应激响应）")
        strategy = cell.handle_failure(1.0 - state.performance, 2.0, 0.4)
        print(f"   → 触发策略: {strategy}")

    # 用户请求需要安全判断
    print("3. 处理用户请求（免疫检查点）")
    allowed, mode = cell.handle_request("边缘请求", 0.6, 0.55)
    status = "允许" if allowed else "拒绝"
    print(f"   → {status}请求，模式={mode}")

    print()
    print("=" * 70)
    print("演示完成！三个P0创新成功协同工作。")
    print()
    print("生物类比总结：")
    print("  • 双重门控 ≈ 突触可塑性：选择性巩固重要记忆")
    print("  • 免疫检查点 ≈ 免疫平衡：动态调节安全阈值")
    print("  • 应激响应 ≈ 细胞应激：分层处理系统故障")
    print("=" * 70)


if __name__ == '__main__':
    demo()
