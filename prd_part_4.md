好的 Sunny，继续输出 **Part 4：Roadmap、数据设计、MVP开发计划、面试表达方式**。

这一部分主要回答：

1. 这个产品未来如何迭代；
2. 一周 MVP 如何真正落地；
3. 如何把它转化成 AI 产品经理面试案例。

---

# Part 4：Roadmap & Execution Plan

# 21. 产品 Roadmap

## Phase 0：MVP Demo（1周）

## 目标

验证：

> 招聘方是否愿意使用 AI 工具辅助判断候选人与岗位匹配程度，并进一步联系候选人。


---

## 核心用户流程

```text
HR收到求职消息

↓

打开AI Job Fit Assistant

↓

输入JD

↓

查看匹配报告

↓

了解候选人经历

↓

点击联系方式

↓

进一步沟通
```

---

## 功能范围

### P0 用户功能

✅ JD输入

✅ JD Requirement Analysis

✅ Hard / Soft Requirement分类

✅ Candidate Knowledge Retrieval

✅ Requirement → Evidence Matching

✅ Unknown Information识别

✅ 简历预览

✅ 联系方式CTA


---

### P0 产品展示

✅ Product Design页面（简版）

展示：

- 为什么做这个产品；
- 用户问题；
- 产品目标；
- Agent Workflow。


---

### P0 数据能力

✅ 基础埋点


---

## MVP不做

❌ 开放式聊天

❌ 多候选人

❌ HR上传简历

❌ 完整后台

❌ 权限系统

❌ 多语言


---

# Phase 1：求职转化优化版

## 目标

提升：

> HR从访问 → 联系的转化率。


---

# 1. Matching Visualization


## 增强匹配结果展示


增加：

### 覆盖率

例如：

```
岗位要求覆盖：

8 / 10
```


---

### 能力分布

例如：

```
AI应用能力

█████


产品能力

████


技术协作

█████
```


---

### Requirement Matrix


例如：

|能力|匹配|证据|
|-|-|-|
|LLM应用|强|POA Workflow|
|Agent|中|Function Calling探索|
|RAG|弱|暂无证据|

---

# 2. Limited Follow-up Agent


目标：

让 HR 深入了解。


例如：

HR：

> 你的Agent经验具体是什么？


Agent：

返回：

OpenCUI + Function Calling相关经历。


---

限制：

只能围绕：

- JD分析结果；
- 候选人知识库。


---

# 3. Unknown Question Loop


## 当前：

Agent发现：

“没有RAG经验证据”。


未来：

自动记录：

```
高频缺失问题：

RAG生产经验
```

---

用途：

优化：

- 简历；
- FAQ；
- 项目展示。


---

# 4. Recruiter Lead Collection


支持：

HR留下联系方式。


例如：

```
姓名：

公司：

邮箱：

想了解的问题：
```


---

价值：

把：

被动等待

变成：

主动跟进。


---

# Phase 2：产品透明化与持续迭代

（替代之前的“AI产品作品集版”）

---

## 目标

展示：

> 我如何持续设计和优化一个AI产品。


---

# 1. Product Evolution

产品迭代记录。


例如：

---

## v0.1

时间：

2026.08


新增：

- JD匹配分析
- Evidence Mapping
- 联系方式CTA


---

## v0.2


新增：

- Unknown信息识别
- 匹配结果可视化


---

## v0.3


优化：

- Prompt策略
- Evaluation机制


---

这个功能价值：

对于 HR：

低。

对于：

AI产品负责人：

高。


---

# 2. Roadmap展示


展示：

未来规划。


例如：

```
已完成：

✓ JD分析

✓ Evidence Matching


计划：

○ 多语言

○ 更强Agent

○ 数据分析

○ 多候选人支持
```

---

# 3. 产品设计文档


展示：

不是传统作品集。

而是：

当前产品的设计过程。


包括：

- PRD
- Agent架构
- Prompt设计
- Evaluation方案


---

# Phase 3：通用招聘助手探索

## 目标

从：

个人求职工具

扩展：

招聘辅助工具。


---

## 功能：

### 多候选人模式

输入：

JD

+

候选人简历


输出：

匹配分析。


---

### 候选人比较

例如：

```
候选人A：

LLM能力强


候选人B：

业务经验强
```


---

### 面试辅助

生成：

- 面试问题；
- 评价维度；
- Follow-up问题。


---

# 22. 数据埋点设计

## 22.1 产品漏斗


核心漏斗：

```text
访问页面

↓

输入JD

↓

生成报告

↓

查看简历

↓

查看项目

↓

点击联系方式
```

---

# 22.2 Event设计


## Page View

事件：

```
page_view
```

记录：

- 时间；
- 来源渠道。


---

## JD Submit

事件：

```
jd_submit
```

记录：

- JD类型；
- 岗位方向；
- 是否成功生成。


---

## Report Generated

事件：

```
report_generated
```


记录：

- 分析耗时；
- 是否异常。


---

## Contact Click

事件：

```
contact_click
```

记录：

- 微信；
- 邮箱。


---

# 22.3 核心指标


## 北极星指标（North Star Metric）

建议：

### 有效沟通转化率


公式：

```
联系方式点击人数
/
报告查看人数
```


原因：

访问量不是目标。

真正目标：

获得招聘沟通。


---

## 辅助指标

### 使用指标：

- JD提交率；
- 报告完成率；
- 平均停留时间。


### AI质量：

- Evidence准确率；
- Unknown识别率；
- 幻觉率。


---

# 23. 一周 MVP 开发计划

假设：

使用：

- Cursor / Codex
- DeepSeek API
- Next.js


---

# Day 1：产品骨架

目标：

页面跑通。


完成：

- 首页；
- JD输入页；
- API调用。


结果：

输入JD：

返回AI文本。


---

# Day 2：知识库准备


整理：

Candidate Profile。


包括：

- 简历；
- 项目；
- FAQ。


转成：

Markdown / JSON。


---

# Day 3：Agent Workflow


完成：

```
JD解析

↓

Requirement分类

↓

Evidence Matching

↓

Report生成
```


---

# Day 4：前端展示


实现：

- 匹配卡片；
- Hard/Soft分类；
- Unknown信息。


---

# Day 5：求职转化


增加：

- 简历查看；
- 联系方式；
- 点击埋点。


---

# Day 6：

优化：

- Prompt；
- 输出稳定性；
- UI。


---

# Day 7：

测试：

找真实用户：

- HR；
- 产品朋友。


观察：

- 是否理解价值；
- 是否愿意点击。


---

# 24. 面试中如何介绍这个项目

这是非常重要的部分。

不要说：

> “我做了一个网站。”

应该说：

> “我发现 AI 产品岗位招聘中，候选人的 AI 能力难以通过传统简历快速体现，因此设计并开发了一个 AI Job Fit Assistant，通过 JD解析、候选人知识检索和 Evidence Matching，帮助招聘方快速判断岗位匹配度，同时验证 AI 在招聘沟通场景中的应用价值。”

---

# STAR表达


## S（Situation）

AI产品岗位要求越来越复杂：

- LLM；
- Agent；
- Evaluation。

但传统简历无法快速体现这些能力。


---

## T（Task）

设计一个工具：

降低招聘方理解候选人的成本。


---

## A（Action）


设计：

### JD解析

识别岗位要求。


### Candidate Knowledge Base

结构化候选人经历。


### Evidence Mapping

建立：

岗位要求 → 项目证据。


### Unknown机制

避免模型幻觉。


---

## R（Result）

MVP阶段：

验证：

- 用户是否愿意使用；
- 哪些信息影响沟通。


指标：

- JD提交量；
- 联系方式点击率；
- 高频缺失问题。


---

# 25. 这个项目最值得强调的 AI PM能力

## 1. AI产品定义能力

不是：

“做一个聊天机器人”。

而是：

发现招聘信息不对称问题。


---

## 2. Agent设计能力

不是：

调用LLM。


而是：

设计：

JD理解 → Retrieval → Evidence Matching。


---

## 3. AI安全与可信设计

体现：

- Unknown机制；
- Evidence grounding；
- 不输出无依据结论。


---

## 4. Evaluation意识

关注：

- 准确率；
- 幻觉；
- 用户转化。


---

# 最终项目定位总结

我认为目前这个项目最好的定位是：

> **一个面向 AI 产品求职场景的 AI Job Fit Assistant，通过 JD 理解、候选人知识库和 Evidence Mapping，帮助招聘方快速判断候选人与岗位匹配程度，同时作为候选人的 AI 产品能力展示载体。**

它不是：

❌ 简历生成器  
❌ 招聘系统  
❌ Chatbot  
❌ AI作品集网站  


它是：

✅ 一个真实场景驱动的 AI 应用 MVP  
✅ 一个可以证明 AI PM 能力的产品案例  
✅ 一个有真实用户和业务指标验证的项目


到这里，PRD 的主要部分已经完整了。

下一步如果继续优化，我觉得最有价值的是两个方向：

1. **把 PRD 压缩成真正开发用的版本（10页以内）**，方便你边开发边参考；
2. **设计具体的 Agent Prompt + Knowledge Base 数据模板**，因为这会直接决定 MVP 一周能不能跑起来。