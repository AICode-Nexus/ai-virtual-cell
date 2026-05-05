# 可解释AI (Explainable AI, XAI)

> 特征归因、局部/全局解释、注意力可视化、概念激活、反事实解释、可解释性评估

## 1. 领域概述

可解释AI（Explainable AI, XAI）关注如何使AI模型的决策过程对人类可理解、可验证、可信任。核心挑战在于：

- **准确性-可解释性权衡**：高性能模型（深度网络）通常是黑盒，简单可解释模型（线性、决策树）性能有限。
- **解释的忠实性**：解释是否真实反映模型内部机制，还是仅是事后合理化。
- **解释的受众适配**：技术人员、领域专家、最终用户对解释的需求和理解能力不同。
- **解释的稳定性**：相似输入是否产生相似解释，解释是否对微小扰动鲁棒。

---

## 2. 核心架构/算法

### 2.1 特征归因方法（Feature Attribution）

- **SHAP（Shapley Additive Explanations）**：基于博弈论Shapley值，为每个特征分配对预测的贡献，满足效率、对称性、虚拟性、可加性公理。
- **LIME（Local Interpretable Model-agnostic Explanations）**：在输入附近采样，训练局部线性代理模型，解释单个预测。
- **积分梯度（Integrated Gradients）**：沿从基线到输入的路径积分梯度，满足完整性公理（归因之和等于预测差）。
- **GradCAM**：利用最后卷积层的梯度生成类激活图，可视化CNN关注的图像区域。
- **LIME vs SHAP**：LIME速度快但局部近似可能不准确；SHAP理论保证更强但计算成本更高。

### 2.2 局部与全局解释（Local and Global Explanations）

- **局部解释**：解释单个预测，回答"为什么模型对这个输入做出这个预测"。
- **全局解释**：理解模型整体行为，回答"模型通常依赖哪些特征/规则"。
- **部分依赖图（PDP）**：展示特征与预测的平均边际关系，揭示全局特征效应。
- **个体条件期望（ICE）**：PDP的个体版本，展示每个样本的特征-预测关系，揭示异质性。
- **全局代理模型**：用可解释模型（决策树、规则集）近似黑盒模型的全局行为。

### 2.3 注意力可视化（Attention Visualization）

- **注意力权重可视化**：展示Transformer中不同位置的注意力权重，直观显示模型关注的输入部分。
- **注意力≠解释的争议**：注意力权重不一定反映因果重要性，可能与梯度归因不一致。
- **注意力流（Attention Flow）**：追踪注意力在多层间的传播，获得更全面的归因。
- **BERTViz**：可视化BERT多头注意力的工具，支持不同粒度的注意力分析。

### 2.4 概念激活向量（Concept Activation Vectors, CAV）

- **TCAV（Testing with CAV）**：学习人类定义概念的方向向量，测试概念对预测的影响程度。
- **概念瓶颈模型（CBM）**：强制模型先预测人类可理解的概念，再基于概念做最终预测。
- **概念发现**：自动从激活空间发现有意义的概念，无需人工标注。
- **优势**：提供高层语义解释，而非低层特征归因。

### 2.5 反事实解释（Counterfactual Explanations）

- **反事实定义**：找到最小的输入变化，使模型改变预测，回答"如果X改变，预测会如何变化"。
- **可行性约束**：反事实应在现实中可实现（如年龄不能减小），需要领域知识约束。
- **多样性**：提供多个不同的反事实，给用户更多改进选择。
- **DICE（Diverse Counterfactual Explanations）**：生成多样化的反事实解释集合。
- **应用场景**：信贷审批、医疗诊断等高风险决策中的申诉与改进指导。

### 2.6 可解释性评估（Explainability Evaluation）

- **忠实性（Faithfulness）**：解释是否真实反映模型行为；通过特征删除测试（删除重要特征后性能下降）评估。
- **稳定性（Stability）**：相似输入的解释是否相似；通过扰动测试评估。
- **可理解性（Comprehensibility）**：人类是否能理解解释；通过用户研究评估。
- **完整性（Completeness）**：解释是否覆盖所有重要因素。
- **ROAR（Remove and Retrain）**：删除归因最重要的特征后重训练，评估归因质量。

---

## 3. 训练或优化机制

- **内在可解释模型**：决策树、线性模型、规则集、广义加性模型（GAM）在训练时即具备可解释性。
- **注意力正则化**：在训练时约束注意力权重与人类标注对齐，提升注意力的解释价值。
- **概念瓶颈训练**：两阶段训练，先学习概念预测，再学习基于概念的任务预测。
- **解释一致性损失**：在训练时加入解释一致性约束，使相似输入产生相似解释。
- **人在回路训练**：利用人类对解释的反馈改进模型，实现解释驱动的模型改进。

---

## 4. 优点、边界与常见失败模式

### 4.1 主要优点

- **信任建立**：可解释性帮助用户理解和信任AI决策，促进实际部署。
- **调试与改进**：解释揭示模型依赖的虚假相关，指导数据收集和模型改进。
- **合规支持**：满足GDPR等法规对"解释权"的要求。

### 4.2 共性边界

- **准确性-可解释性权衡**：最可解释的模型通常不是最准确的。
- **解释的主观性**：不同解释方法可能给出不同甚至矛盾的解释。
- **计算成本**：SHAP等方法在大规模数据上计算成本高。

### 4.3 典型失败模式

- **解释不忠实**：解释与模型实际决策机制不符，产生误导性理解。
- **解释不稳定**：微小输入扰动导致解释剧烈变化，降低可信度。
- **注意力误导**：注意力权重被误解为因果重要性，导致错误结论。
- **反事实不可行**：生成的反事实在现实中无法实现，缺乏实用价值。
- **过度简化**：局部线性近似无法捕获复杂非线性关系，解释失真。

---

## 5. 与其他AI领域的交叉关系

- **与深度神经网络架构**：Transformer注意力机制是可视化的主要对象，CNN激活图是视觉解释的基础。
- **与因果推理**：因果解释比相关性解释更忠实，反事实解释与因果推理天然结合。
- **与安全对齐**：可解释性是AI对齐的重要工具，帮助识别模型的不当行为。
- **与强化学习**：策略可解释性帮助理解智能体决策，支持人机协作。
- **与知识表示**：概念激活向量将神经网络表示与人类概念对齐。

---

## 6. 代表性系统或论文方向

- **特征归因**：SHAP（Lundberg 2017）、LIME（Ribeiro 2016）、积分梯度（Sundararajan 2017）。
- **视觉解释**：GradCAM（Selvaraju 2017）、RISE（Petsiuk 2018）。
- **概念解释**：TCAV（Kim 2018）、概念瓶颈模型（Koh 2020）。
- **反事实解释**：DICE（Mothilal 2020）、FACE（Poyiadzi 2020）。
- **工具框架**：SHAP库、Captum（PyTorch可解释性）、InterpretML（微软）。

---

## 7. 技术要点速览（机制级）

1. SHAP基于Shapley值为每个特征分配对预测的公平贡献。
2. LIME在局部训练线性代理模型，解释单个预测。
3. 积分梯度满足完整性公理，归因之和等于预测与基线的差。
4. GradCAM利用梯度生成类激活图，可视化CNN关注区域。
5. 注意力权重不等于因果重要性，需谨慎解读。
6. TCAV测试人类定义概念对预测的影响程度。
7. 概念瓶颈模型强制通过人类概念进行预测，提供高层解释。
8. 反事实解释回答"如何改变输入使预测改变"。
9. 反事实可行性约束确保解释在现实中可实现。
10. 忠实性是解释质量的核心指标，通过特征删除测试评估。
11. 稳定性确保相似输入产生相似解释。
12. 全局代理模型用可解释模型近似黑盒模型整体行为。
13. 部分依赖图展示特征与预测的平均边际关系。
14. 解释一致性损失在训练时约束解释稳定性。
15. 人在回路训练利用解释反馈改进模型。
16. 准确性-可解释性权衡是XAI的核心挑战。
17. 不同解释方法可能给出矛盾结论，需要多方法交叉验证。
18. GDPR等法规推动可解释性成为高风险AI的必要条件。
19. 内在可解释模型在训练时即具备可解释性，无需事后解释。
20. 解释的受众适配需要根据用户背景调整解释粒度和形式。

---

## 8. 参考来源

### A类证据（权威综述/教材/官方）

- Molnar, C. (2022). *Interpretable Machine Learning* (2nd ed.). https://christophm.github.io/interpretable-ml-book/
- Arrieta, A. B., et al. (2020). Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges. *Information Fusion*, 58, 82-115.
- DARPA XAI Program: https://www.darpa.mil/program/explainable-artificial-intelligence

### B类证据（代表性论文）

- Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions (SHAP). *NeurIPS 2017*.
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier (LIME). *KDD 2016*.
- Selvaraju, R. R., et al. (2017). Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization. *ICCV 2017*.
- Sundararajan, M., Taly, A., & Yan, Q. (2017). Axiomatic Attribution for Deep Networks (Integrated Gradients). *ICML 2017*.
- Kim, B., et al. (2018). Interpretability Beyond Classification Output: Semantic Bottleneck Networks (TCAV). *ICML 2018*.

### 官方技术文档

- SHAP库: https://shap.readthedocs.io/
- Captum（PyTorch可解释性）: https://captum.ai/
- InterpretML（微软）: https://interpret.ml/
