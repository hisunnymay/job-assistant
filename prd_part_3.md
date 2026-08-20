好的 Sunny，继续 **Part 3：Agent 设计、知识库设计、技术架构、Evaluation 方案**。

这一部分我会稍微偏 AI PM 视角，因为它会是你未来面试时最有价值的部分：

> “你为什么这样设计 Agent，而不是简单调用 LLM？”

---

# Part 3：Agent & Technical Design

# 13. Agent 总体设计

## 13.1 设计目标

AI Job Fit Assistant 的核心不是生成一段自然语言回答，而是完成：

> JD需求理解 → 候选人信息检索 → 证据匹配 → 可解释输出

因此采用：

**Workflow-based Agent**

而不是：

开放式 Chatbot。

---

# 13.2 Agent Workflow


整体流程：

```text
User Input

(JD)

↓

Agent 1:
JD Requirement Parser

↓

Agent 2:
Requirement Classifier

↓

Agent 3:
Candidate Evidence Retriever

↓

Agent 4:
Matching Analyzer

↓

Agent 5:
Report Generator

↓

Structured Response
```


---

# 14. Agent模块设计


# 14.1 JD Requirement Parser


## 输入

用户输入：

岗位 JD。


例如：

```
负责AI产品规划设计；
熟悉LLM、Agent相关技术；
具备3年以上产品经验；
具备快速学习能力。
```


---

## 输出

结构化岗位要求。


例如：

```json
{
"requirements":[
 {
  "text":"3年以上产品经验",
  "type":"hard",
  "category":"experience"
 },
 {
  "text":"熟悉LLM、Agent",
  "type":"hard",
  "category":"technical"
 },
 {
  "text":"快速学习能力",
  "type":"soft",
  "category":"behavior"
 }
]
}
```

---

## 产品价值

把非结构化 JD 转换成：

机器可以处理的能力模型。

---

# 14.2 Requirement Classifier


## 目标

判断：

这个要求属于：

- Hard Requirement
- Soft Requirement


---

## 分类逻辑


### Hard Requirement

特点：

可验证事实。


例如：

“3年以上产品经验”

证据：

简历。


---

### Soft Requirement

特点：

行为倾向。


例如：

“有主人翁意识”


证据：

项目经历。


---

## 边界情况

例如：

“优秀沟通能力”


可能：

Soft。


但如果：

“有跨部门项目管理经验”

偏 Hard。


所以：

允许：

```json
{
"type":"uncertain"
}
```

避免强制分类。

---

# 14.3 Candidate Evidence Retriever


## 目标

从候选人知识库找到相关证据。


---

## 不采用：

关键词搜索。


例如：

JD：

“Agent经验”


知识库：

“使用OpenCUI搭建交易型对话机器人，并探索Function Calling能力。”


关键词：

没有 Agent。


但是语义相关。


---

## 推荐方案：

Embedding Retrieval + LLM判断。


流程：

```
Requirement

↓

Vector Search

↓

Relevant Evidence

↓

LLM验证相关性

↓

Return Evidence
```

---

# 14.4 Matching Analyzer


## 输入

岗位要求：

```
Requirement:
LLM应用经验
```


证据：

```
POA项目：
使用Dify搭建LLM Workflow
```


---

## 输出：

```json
{
"status":"strong_match",

"reason":
"候选人具有企业场景LLM Workflow落地经验",

"evidence":
"POA授权信息提取项目"
}
```

---

# 14.5 Report Generator


## 任务

将结构化结果转换为：

HR 可阅读报告。


---

## 注意：

这里不要让 LLM 自由发挥。


推荐：

结构：

```json
{
summary:{},

hard_requirements:[],

soft_requirements:[],

gaps:[]
}
```


前端负责展示。


---

# 15. Candidate Knowledge Base设计


这是整个产品质量的核心。

---

# 15.1 为什么不能只上传简历？

因为：

简历适合：

事实。


但 AI PM 面试需要：

思考过程。


例如：

简历：

> 使用Dify搭建LLM Workflow。


但是面试官想知道：

> 为什么这样设计？
> 为什么不用规则？
> 如何评估效果？


所以需要扩展知识库。


---

# 15.2 Knowledge Base结构


## Layer 1：Resume Facts


存储：

客观事实。


例如：

```json
{
"type":"experience",

"company":"滴滴",

"role":"产品经理",

"duration":"2025.11-2026.07"
}
```

---

## Layer 2：Project Evidence


这是最重要。


结构：

```json
{
"project":"POA LLM信息抽取",

"background":
"线下POA管理效率低",

"problem":
"人工审核成本高",

"solution":
"搭建LLM Workflow",

"technology":
[
"Dify",
"LLM",
"OCR"
],

"result":
"上线使用"
}
```


---

## Layer 3：Interview FAQ


例如：

问题：

> 为什么从传统产品转AI？


回答：

结构化保存。


---

## Layer 4：Product Thinking


例如：

问题：

> 为什么没有直接使用Agent，而使用Workflow？


回答：

记录：

产品判断逻辑。


---

# 16. MVP技术架构


考虑：

一周完成。

目标：

简单、可迭代。


---

# 16.1 推荐架构


```text
Frontend

Next.js / React

        |

Backend API

Node / Python

        |

LLM Service

DeepSeek / OpenAI API

        |

Knowledge Base

Markdown / JSON

        |

Vector Database (Future)
```


---

# MVP简化：

甚至可以：

```text
Frontend

↓

Backend

↓

Prompt + JSON Knowledge Base

↓

LLM
```


不用一开始上：

- LangChain；
- Agent Framework；
- Vector DB。


---

原因：

你的知识库规模非常小。

几十个项目事实。

完全可以：

Prompt + Structured Context。


---

# 17. MVP Prompt设计原则


不要：

一个大 Prompt：

> 你是招聘专家，请分析。


---

推荐：

拆分任务。


---

## Prompt 1

JD解析。


目标：

结构化。


---

## Prompt 2

匹配判断。


目标：

Evidence Mapping。


---

## Prompt 3

报告生成。


目标：

用户体验。


---

这样未来：

替换模型：

成本更低。


---

# 18. 数据结构设计（建议）


## Requirement

```json
{
"id":"req_001",

"text":"LLM应用经验",

"type":"hard",

"category":"technical"
}
```

---

## Evidence

```json
{
"id":"exp_001",

"source":"POA项目",

"content":
"搭建LLM信息抽取Workflow",

"skills":
[
"LLM",
"Prompt",
"Workflow"
]
}
```

---

## Match Result

```json
{
"requirement_id":"req_001",

"status":"strong_match",

"evidence_ids":
[
"exp_001"
],

"confidence":"high"
}
```

---

# 19. Evaluation设计

这个部分非常重要。

因为 AI PM 面试一定可能问：

> 你怎么知道这个 Agent 做得好？


---

# 19.1 不评价“回答好不好”

太主观。


评价：

任务完成情况。


---

# Metric 1：Requirement Extraction Accuracy


问题：

JD要求有没有正确提取？


测试：

人工标注：

100条JD要求。


比较：

AI结果。


---

# Metric 2：Evidence Retrieval Accuracy


问题：

找到的证据是否相关？


例如：

Requirement：

LLM经验。


返回：

POA项目。

正确。


---

# Metric 3：Hallucination Rate


问题：

有没有编造经历？


例如：

错误：

> 候选人负责RAG系统上线。


如果没有：

必须避免。


---

# Metric 4：Contact Conversion Rate


这是你的业务指标。


最终：

不是模型准确率。


而是：

```text
访问人数

↓

分析人数

↓

联系方式点击人数
```


---

# 20. 为什么这个设计体现AI PM能力？


这个项目可以回答很多面试问题。

---

## Q：

为什么不用普通ChatGPT？


回答：

因为招聘匹配需要：

- 结构化JD解析；
- 候选人知识检索；
- 证据映射；
- 可解释输出。


---

## Q：

为什么不直接输出匹配分？


回答：

因为LLM评分缺少透明度。

招聘场景需要：

Evidence-based decision support。


---

## Q：

为什么区分Hard和Soft？


回答：

因为：

事实能力和行为能力的证据来源不同。

需要不同判断逻辑。


---

## Q：

如何减少幻觉？


回答：

- Knowledge grounding；
- Evidence retrieval；
- Unknown机制；
- 不允许无证据推断。


---

# Part 3 总结

这个产品的核心 AI 设计：

不是：

> “我调用了一个大模型。”

而是：

> “我设计了一个基于候选人知识库的 Evidence Matching Agent，用结构化推理帮助招聘方降低筛选成本。”

这句话未来可以直接作为你的面试项目介绍。

---

下一部分 **Part 4（最后部分）** 我会整理：

1. Roadmap（根据我们最新讨论调整）
2. 产品迭代记录设计
3. 数据埋点方案
4. MVP开发计划（一周拆解）
5. 面试中如何讲这个项目（STAR + AI PM版本）

这一部分会更偏落地执行。