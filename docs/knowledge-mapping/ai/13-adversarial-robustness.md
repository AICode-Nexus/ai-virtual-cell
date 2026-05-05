# 对抗鲁棒性 (Adversarial Robustness)

> 对抗样本、攻击方法、防御机制、认证鲁棒性、分布外泛化、鲁棒性评估

## 1. 领域概述

对抗鲁棒性关注AI模型在面对恶意扰动、分布偏移和极端输入时的可靠性。核心挑战在于：

- **对抗脆弱性**：深度神经网络对人类不可察觉的微小扰动极度敏感，导致错误预测。
- **攻击-防御军备竞赛**：新防御方法不断被新攻击方法突破，难以达到绝对安全。
- **认证鲁棒性**：提供可证明的鲁棒性保证，而非仅凭经验评估。
- **鲁棒性-准确性权衡**：提升对抗鲁棒性通常以牺牲标准准确率为代价。

---

## 2. 核心架构/算法

### 2.1 对抗样本与攻击方法（Adversarial Examples and Attacks）

- **FGSM（Fast Gradient Sign Method）**：沿损失函数梯度符号方向添加扰动，单步攻击，速度快但强度有限。
- **PGD（Projected Gradient Descent）**：多步迭代FGSM，每步投影回ε球内，是最强的一阶攻击之一。
- **C&W攻击**：优化扰动最小化同时使分类错误，可绕过梯度掩蔽防御。
- **AutoAttack**：集成多种攻击（APGD-CE、APGD-DLR、FAB、Square Attack），提供可靠的鲁棒性评估。
- **黑盒攻击**：无需访问模型梯度，通过查询（决策边界攻击）或迁移性（用代理模型生成对抗样本）实现。
- **物理世界攻击**：在真实物理环境中实现的对抗扰动（对抗贴纸、对抗眼镜），对自动驾驶等安全关键系统威胁大。

### 2.2 防御机制（Defense Mechanisms）

- **对抗训练（Adversarial Training）**：在训练时加入对抗样本，是目前最有效的经验防御方法；PGD对抗训练是标准基线。
- **随机平滑（Randomized Smoothing）**：对输入添加高斯噪声后取多数投票，提供可认证的L2鲁棒性保证。
- **输入预处理**：去噪、JPEG压缩、特征压缩等预处理方法，但通常可被自适应攻击绕过。
- **检测方法**：训练对抗样本检测器，拒绝可疑输入；但检测器本身也可能被攻击。
- **集成防御**：多个模型集成，利用多样性降低攻击成功率。
- **梯度掩蔽（Gradient Masking）**：使梯度不可用或不准确，但通常只是表面防御，可被黑盒攻击绕过。

### 2.3 认证鲁棒性（Certified Robustness）

- **完全验证（Complete Verification）**：精确计算模型在扰动球内的最坏情况输出，计算成本随网络规模指数增长。
- **不完全验证（Incomplete Verification）**：通过凸松弛（IBP、CROWN、α-CROWN）提供鲁棒性下界，计算效率更高。
- **随机平滑认证**：基于统计的认证方法，提供高概率的L2鲁棒性保证，可扩展到大规模网络。
- **认证训练**：在训练时直接优化认证鲁棒性下界，提升认证鲁棒性。
- **认证半径**：在给定扰动范围内保证预测不变的最大扰动量，是认证鲁棒性的核心指标。

### 2.4 分布外泛化（Out-of-Distribution Generalization）

- **数据增强**：通过多样化训练数据（颜色抖动、几何变换、Mixup、CutMix）提升分布鲁棒性。
- **域泛化（Domain Generalization）**：在多个源域上训练，泛化到未见目标域；不变风险最小化（IRM）学习跨域不变特征。
- **OOD检测**：识别测试样本是否来自训练分布，拒绝或标记分布外输入。
- **最大似然估计的局限**：标准ERM在分布偏移下泛化能力有限，需要专门的鲁棒优化方法。

### 2.5 后门攻击与防御（Backdoor Attacks and Defenses）

- **后门攻击**：在训练数据中注入带触发器的中毒样本，使模型在触发器存在时产生错误预测。
- **触发器设计**：可见触发器（贴纸）、不可见触发器（频域扰动）、语义触发器（特定属性）。
- **后门检测**：Neural Cleanse（逆向工程触发器）、STRIP（运行时检测）、Spectral Signatures（激活分析）。
- **数据清洗**：识别并移除训练集中的中毒样本，需要在无干净参考数据时工作。

### 2.6 鲁棒性评估（Robustness Evaluation）

- **RobustBench**：标准化的对抗鲁棒性评估基准，使用AutoAttack评估，提供可比较的排行榜。
- **鲁棒准确率**：在对抗样本上的准确率，是经验鲁棒性的核心指标。
- **认证准确率**：可认证鲁棒的样本比例，是认证鲁棒性的核心指标。
- **自适应攻击评估**：针对特定防御设计的攻击，避免虚假的安全感。
- **多威胁模型评估**：在L∞、L2、L1等不同范数约束下评估，全面评估鲁棒性。

---

## 3. 训练或优化机制

- **PGD对抗训练**：内循环生成对抗样本，外循环最小化对抗损失，是标准对抗训练方法。
- **TRADES**：平衡标准准确率和对抗鲁棒性，通过KL散度约束自然样本和对抗样本预测的一致性。
- **认证训练（IBP/CROWN-IBP）**：直接优化认证鲁棒性下界，提升认证准确率。
- **数据增强策略**：AutoAugment、RandAugment等自动增强策略提升分布鲁棒性。
- **预训练的鲁棒性迁移**：在大规模数据上预训练的模型通常具有更好的鲁棒性基础。

---

## 4. 优点、边界与常见失败模式

### 4.1 主要优点

- **安全保障**：对抗训练显著提升模型在恶意攻击下的可靠性。
- **可证明保证**：认证鲁棒性提供数学上可证明的安全边界。
- **泛化提升**：对抗训练通常也提升模型在自然分布偏移下的鲁棒性。

### 4.2 共性边界

- **鲁棒性-准确性权衡**：提升对抗鲁棒性通常以牺牲标准准确率为代价。
- **计算成本高**：对抗训练需要多步内循环，训练时间增加3-10倍。
- **认证方法可扩展性有限**：完全验证在大规模网络上计算不可行。

### 4.3 典型失败模式

- **梯度掩蔽假安全**：防御方法使梯度不可用，但被黑盒攻击轻易绕过。
- **自适应攻击突破**：针对特定防御设计的攻击通常能突破该防御。
- **过拟合对抗样本**：对抗训练可能过拟合特定攻击类型，对其他攻击仍脆弱。
- **认证-实际差距**：认证鲁棒性下界与实际鲁棒性之间存在差距。
- **物理世界迁移失败**：数字域对抗样本在物理世界中效果可能减弱。

---

## 5. 与其他AI领域的交叉关系

- **与深度神经网络架构**：架构选择影响对抗脆弱性，ViT通常比CNN更鲁棒。
- **与可解释AI**：对抗样本揭示模型依赖的虚假特征，推动可解释性研究。
- **与安全对齐**：对抗鲁棒性是AI安全的基础，防止恶意用户操纵模型输出。
- **与联邦学习**：联邦学习中的拜占庭攻击是对抗鲁棒性在分布式场景的扩展。
- **与因果推理**：因果特征通常比相关特征更鲁棒，因果方法可提升分布外泛化。

---

## 6. 代表性系统或论文方向

- **攻击方法**：FGSM（Goodfellow 2015）、PGD（Madry 2018）、C&W（Carlini 2017）、AutoAttack（Croce 2020）。
- **防御方法**：PGD对抗训练（Madry 2018）、TRADES（Zhang 2019）、随机平滑（Cohen 2019）。
- **认证方法**：IBP（Gowal 2018）、CROWN（Zhang 2018）、α-CROWN（Wang 2021）。
- **评估基准**：RobustBench（Croce 2021）、OOD-Bench（Ye 2022）。
- **后门防御**：Neural Cleanse（Wang 2019）、STRIP（Gao 2019）。

---

## 7. 技术要点速览（机制级）

1. FGSM沿梯度符号方向添加扰动，单步快速但强度有限。
2. PGD多步迭代并投影回扰动球，是最强的一阶攻击之一。
3. AutoAttack集成多种攻击，提供可靠的鲁棒性评估基准。
4. 对抗训练在训练时加入对抗样本，是最有效的经验防御。
5. 随机平滑通过高斯噪声和多数投票提供可认证的L2鲁棒性。
6. 梯度掩蔽只是表面防御，可被黑盒攻击绕过。
7. 认证鲁棒性提供数学上可证明的安全保证。
8. IBP/CROWN通过凸松弛提供鲁棒性下界，计算效率高于完全验证。
9. 鲁棒性-准确性权衡是对抗鲁棒性的核心挑战。
10. 自适应攻击评估是验证防御有效性的必要步骤。
11. 后门攻击通过训练数据中毒植入触发器。
12. Neural Cleanse通过逆向工程检测后门触发器。
13. 域泛化学习跨域不变特征，提升分布外泛化能力。
14. OOD检测识别分布外输入，避免不可靠预测。
15. 物理世界攻击对自动驾驶等安全关键系统威胁大。
16. 预训练模型通常具有更好的鲁棒性基础。
17. TRADES平衡标准准确率和对抗鲁棒性。
18. 认证训练直接优化认证鲁棒性下界。
19. RobustBench提供标准化的鲁棒性排行榜。
20. 对抗样本揭示模型依赖的虚假相关特征。

---

## 8. 参考来源

### A类证据（权威综述/教材/官方）

- Goodfellow, I., McDaniel, P., & Papernot, N. (2018). Making machine learning robust against adversarial inputs. *Communications of the ACM*, 61(7), 56-66.
- Croce, F., et al. (2021). RobustBench: a standardized adversarial robustness benchmark. *NeurIPS 2021 Datasets and Benchmarks*.
- Madry, A., et al. (2018). Towards Deep Learning Models Resistant to Adversarial Attacks. *ICLR 2018*.

### B类证据（代表性论文）

- Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). Explaining and Harnessing Adversarial Examples (FGSM). *ICLR 2015*.
- Carlini, N., & Wagner, D. (2017). Towards Evaluating the Robustness of Neural Networks (C&W). *IEEE S&P 2017*.
- Cohen, J., Rosenfeld, E., & Kolter, Z. (2019). Certified Adversarial Robustness via Randomized Smoothing. *ICML 2019*.
- Zhang, H., et al. (2019). Theoretically Principled Trade-off between Robustness and Accuracy (TRADES). *ICML 2019*.

### 官方技术文档

- Foolbox（对抗攻击库）: https://foolbox.readthedocs.io/
- CleverHans: https://github.com/cleverhans-lab/cleverhans
- auto_LiRPA（认证验证库）: https://github.com/Verified-Intelligence/auto_LiRPA
