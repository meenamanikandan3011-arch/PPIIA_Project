# Flowise Setup Guide – Public Policy Insight & Impact Analyzer

This document explains how to recreate the Flowise AI pipeline
used in this project.

> Note: Flowise Cloud currently does not support exporting flow JSON.
> This guide provides step-by-step instructions to rebuild the flow.

---

## Platform
- Flowise Cloud (https://cloud.flowiseai.com)

---

## Step 1: Create New Canvas
1. Login to Flowise Cloud
2. Click **Create New Chatflow**
3. Name it: `Public_Policy_Insight`

---

## Step 2: Add LLM Node (ChatGroq)

1. Click **Add Node**
2. Select **ChatGroq**
3. Configure:
   - API Key: Groq API Key
   - Model: `llama3-8b-instant`
   - Temperature: `0.3`

---

## Step 3: Add Memory

1. Add **Buffer Memory** node
2. Keep default settings

---

## Step 4: Add Chat Engine

1. Add **Simple Chat Engine**
2. Connect:
   - ChatGroq → Chat Model
   - Buffer Memory → Memory
3. Paste system prompt from `prompts.md` into **System Message**

---

## Step 5: Connect Nodes

Final flow connection:

ChatGroq  
→ Simple Chat Engine (Chat Model)

Buffer Memory  
→ Simple Chat Engine (Memory)

---

## Step 6: Test the Flow

Example input:
Analyze the following bill:
[Paste bill text here]
