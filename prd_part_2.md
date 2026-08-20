好的 Sunny，继续输出 **Part 2：详细功能设计**。

这一部分会更接近真正开发前的 PRD，包括：

- 页面结构；
- 用户操作流程；
- Agent 输入输出；
- 匹配逻辑；
- 信息展示方式。

---

# Part 2：详细功能设计

# 7. 产品整体信息架构

MVP 页面结构：

```text
AI Job Fit Assistant

├── 首页 Landing Page
│
├── JD Match Analysis
│   ├── JD输入
│   ├── 分析过程
│   └── 匹配报告
│
├── Resume Overview
│
├── Product Design
│
└── Contact
```

---

# 8. 页面设计

# 8.1 首页 Landing Page

## 页面目标

让 HR 在 5 秒内理解：

1. 这是什么？
2. 为什么值得使用？
3. 下一步做什么？


---

## 页面内容

### Header

```
AI岗位匹配助手

AI-powered Job Fit Analysis
```

副标题：

> 输入岗位 JD，快速了解候选人与岗位需求的匹配程度。


---

## 核心价值说明

展示：

```
通过 AI 分析：

✓ 岗位核心要求
✓ 候选人匹配证据
✓ 潜在信息缺口
✓ 建议进一步沟通方向
```

---

## CTA

按钮：

```
开始分析岗位
```

点击：

进入 JD 输入页面。

---

## 页面底部

轻量展示：

```
Created by 梅唱

AI Product Manager
```

注意：

个人信息不是主品牌。

目标：

让 HR 记住产品，同时知道背后是谁。

---

# 8.2 JD 输入页面

## 用户目标

HR 粘贴岗位 JD。


---

## 输入框

字段：

### JD Content

必填。

Placeholder：

```
请粘贴岗位JD，例如：

负责AI产品规划设计；
熟悉LLM、Agent应用；
具备3年以上产品经验...
```

---

MVP 不要求：

- 公司名称；
- 岗位名称；
- 联系方式。


原因：

减少用户操作成本。


---

## 提交按钮

```
开始分析
```

---

# 8.3 JD Requirement Analysis

## Agent任务

将 JD 转换为结构化要求。


---

## 输入

原始 JD：

```
负责AI产品设计，
熟悉LLM、Prompt、Agent，
有3年以上产品经验，
具备快速学习能力...
```

---

## 输出结构

```json
{
 "hard_requirements": [
   {
    "requirement":"3年以上产品经验",
    "category":"experience"
   },
   {
    "requirement":"LLM应用经验",
    "category":"technical"
   }
 ],

 "soft_requirements":[
   {
    "requirement":"快速学习能力",
    "category":"behavior"
   }
 ]
}
```

---

# 8.4 Candidate Knowledge Retrieval

## Agent任务

根据岗位要求，从候选人知识库寻找相关证据。


---

## 检索原则：

不是：

关键词匹配。


而是：

语义匹配。


例如：

JD：

> 熟悉 Agent


知识库：

> 使用 OpenCUI 平台搭建交易型对话机器人，并探索 Function Calling 在业务流程中的应用。


虽然没有完全相同关键词：

Agent仍然应该认为：

存在相关证据。

---

# 8.5 Matching Report（核心页面）


这是 HR 最主要看到的页面。


整体结构：

```
岗位匹配分析报告

↓

总体概览

↓

硬性要求匹配

↓

软性要求匹配

↓

信息缺口

↓

联系方式
```

---

# 9. 匹配报告设计

# 9.1 总体概览


## 目标：

让 HR 快速判断。


展示：

```
岗位分析完成

共识别：
10项岗位要求


已找到匹配证据：
8项


其中：

强匹配：
5项

部分匹配：
3项

暂无证据：
2项
```


---

注意：

不使用：

“综合评分 85分”。


原因：

LLM评分缺乏解释性。


采用：

Evidence Coverage。


---

# 9.2 Hard Requirement Matching


## 展示形式

卡片。


例如：

---

## LLM应用经验

状态：

🟢 强匹配


证据：

```
候选人在POA项目中：

基于Dify搭建文件上传 → OCR → LLM信息提取 → 授权信息匹配 Workflow。

通过Prompt优化和数据标注持续优化模型效果。
```

---

来源：

```
项目：
POA授权管理线上化与LLM信息抽取
```

---

## Agent经验

状态：

🟡 部分匹配


证据：

```
具备：

- Function Calling能力验证经验
- 对话机器人搭建经验

但：

暂无生产级Multi-Agent系统经验。
```

---

这个设计非常重要。

因为它不会隐藏不足。

反而体现：

模型边界判断能力。

---

# 9.3 Soft Requirement Matching


软能力单独展示。


原因：

软能力不是事实证明。


---

例如：

## 探索精神

状态：

🟢 较强匹配


依据：

```
候选人主动探索：

- LLM Workflow
- Prompt优化
- Cursor/Codex辅助开发

并将AI能力应用于实际业务场景。
```

---

## 快速学习能力

状态：

🟢 较强匹配


依据：

```
从传统产品方向逐步扩展：

对话机器人
→ LLM应用
→ 模型评测
→ AI Agent探索
```

---

注意：

这里用：

“依据”

而不是：

“证明”。

因为软能力只能推断。


---

# 9.4 Information Gap（信息缺口）


这是一个非常重要的 AI 可信度设计。


展示：

```
以下岗位要求暂无充分证据：

1.

RAG生产实践

当前信息：
未找到相关项目经历


2.

大规模Agent系统设计

当前信息：
具备Workflow经验，
但未体现复杂Agent架构经验。
```


---

价值：

### 对HR：

知道下一步应该问什么。


### 对候选人：

知道未来补充什么。


---

# 9.5 Resume Preview


入口：

```
查看候选人完整经历
```

---

展示：

## 基础信息

- 产品经验年限
- AI方向
- 技术能力


## 项目列表

例如：

### POA LLM信息抽取

### Lucy大模型评测平台

### OpenCUI智能对话机器人


---

# 9.6 Contact CTA


这是业务目标。


页面底部：

```
如果您认为候选人与岗位需求匹配：

欢迎进一步沟通


[复制邮箱]

[复制微信]
```

---

点击后：

记录事件：

```json
{
 event:"contact_click",
 type:"wechat"
}
```

---

# 10. Limited Follow-up Agent（Future）


虽然不是 MVP，但提前定义。


定位：

不是聊天机器人。


而是：

> 基于匹配报告的解释助手。


---

允许：

### 追问：

```
为什么认为候选人有LLM经验？
```

回答：

基于证据。


---

### 展开：

```
详细介绍POA项目
```

返回：

项目详情。


---

禁止：

```
帮我分析另一个候选人
```

```
帮我写招聘JD
```

---

# 11. Product Design 页面（MVP简版）


目标：

给招聘经理/面试官查看。


---

内容：

## Why

为什么做：

招聘沟通存在信息不对称。


---

## User Problem

HR：

快速判断候选人匹配困难。


---

## Solution

JD解析：

↓

Candidate Knowledge Retrieval

↓

Evidence Mapping


---

## Agent Workflow

展示：

```
JD Parser

↓

Requirement Classifier

↓

Knowledge Retrieval

↓

Matching

↓

Report Generation
```

---

# 12. MVP用户流程总结


完整流程：

```text
HR收到求职消息

↓

点击链接

↓

首页理解价值

↓

粘贴JD

↓

AI分析

↓

查看匹配报告

↓

发现匹配证据

↓

查看简历/项目

↓

点击联系方式

↓

进一步沟通
```

---

# Part 2 总结

MVP核心不是：

“做一个聊天机器人”。

而是：

> 一个基于 Evidence Mapping 的 AI 岗位匹配分析工具。


核心差异：

传统：

```
JD
+
简历

↓

人工判断
```

你的产品：

```
JD

↓

Requirement Understanding

+

Candidate Knowledge

↓

Evidence Mapping

↓

Explainable Matching Report
```

---

下一部分 **Part 3** 我会继续整理：

1. Agent Workflow 详细设计  
2. Candidate Knowledge Base 数据结构  
3. Prompt 设计思路  
4. 技术架构（适合一周 MVP 的实现方案）  
5. 如何设计 Evaluation，避免“LLM自嗨”  

这部分会比较贴近你之后面试 AI PM 时可以讲的内容。