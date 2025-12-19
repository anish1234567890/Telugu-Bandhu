````markdown
# Architecture & Design Document: Telangana Bandhu Agent

## 1. System Overview
**Telangana Bandhu** is a voice-first, agentic AI system designed to assist citizens in identifying and applying for government welfare schemes in the **Telugu** language. Unlike simple chatbots, it utilizes a sophisticated **Agentic Workflow** (Planner–Executor–Evaluator) to autonomously reason about user inputs, missing information, and tool usage.

### Core Technology Stack (Free Tier)
- **Orchestrator:** LangGraph (State Machine Management)
- **LLM (Brain):** Llama 3.3 70B Versatile (via Groq API)
- **Speech-to-Text (STT):** Whisper Large V3 (via Groq API)
- **Text-to-Speech (TTS):** Edge TTS (Microsoft Neural Voices)
- **Tools:** Python-based logic for scheme eligibility and information retrieval

---

## 2. High-Level Architecture Diagram

The system follows a modular **voice-first pipeline**, where audio is the primary input and output interface.

```mermaid
graph TD
    User((User)) <-->|Voice| AudioInterface[Voice Interface]

    subgraph "Local Client"
        AudioInterface -->|Audio .wav| STT[Groq Whisper STT]
        TTS[Edge TTS] -->|Audio .mp3| AudioInterface
    end

    subgraph "Agent Core (LangGraph)"
        STT -->|Text| State[Agent State]
        State --> Planner[Llama 3.3 LLM]
        Planner -->|Decision| Router{Check Intent}

        Router -->|Need Info?| Tools[Scheme Tools]
        Router -->|Direct Answer| Generator[Response Generator]

        Tools -->|Data| Planner
        Generator -->|Telugu Text| TTS
    end
````

---

## 3. Agent Lifecycle & Decision Flow

The agent operates on a continuous **Listen → Think → Act → Speak** loop.

### Lifecycle Stages

1. **Listening:** Records user audio until silence or stop signal.
2. **Transcription:** Audio is sent to Groq Whisper for Telugu speech-to-text.
3. **Reasoning:**

   * Llama 3.3 analyzes user intent using system prompts.
   * Checks whether required details (age, occupation, land size) are present.
4. **Tool Execution:**

   * If data is missing, the agent asks clarifying questions.
   * If data is complete, it calls eligibility or information tools.
5. **Synthesis:** Final response is converted to Telugu speech using Edge TTS.

### Decision Flowchart

```mermaid
flowchart TD
    Start([User Speaks]) --> Transcribe[STT: Speech to Text]
    Transcribe --> LLM[LLM Reasoning]

    LLM --> Check{Is Info Complete?}

    Check -- No --> AskUser[Generate Clarifying Question]
    AskUser --> Speak[TTS Output]

    Check -- Yes --> CallTool[Call Tool: check_eligibility]
    CallTool --> Result[Tool Output]
    Result --> LLM2[Synthesize Answer]
    LLM2 --> Speak

    Speak --> Start
```

---

## 4. Memory & State Management

The agent maintains conversational context using **LangGraph State Management**.

* **State Structure:** `AgentState` containing a list of messages
* **Persistence:** Entire conversation history is passed to the LLM at every turn
* **Conflict Handling:** If contradictory inputs are detected, the LLM resolves them using prior context

```python
class AgentState(BaseModel):
    messages: Annotated[List, add_messages] = []
```

---

## 5. System Prompts & Persona

The agent’s behavior is governed by a carefully designed **system prompt**, enforcing language, tone, and operational rules.

### System Prompt (Persona)

> **Role:** You are “Telangana Bandhu”, a helpful government service agent for the state of Telangana.
>
> **Mandatory Rules:**
>
> 1. **LANGUAGE:** Respond ONLY in Telugu (Telugu script).
> 2. **GOAL:** Help citizens understand and check eligibility for welfare schemes.
> 3. **BEHAVIOR:**
>
>    * Be polite and respectful (use “గారు”).
>    * Ask for missing details one at a time.
> 4. **TOOL USAGE:**
>
>    * Call `check_eligibility` only when age, occupation, and land details are known.
>    * Call `get_scheme_details` for general scheme information.
> 5. **CONCISENESS:** Limit spoken responses to 2–3 sentences.

### Tool Definitions

* **check_eligibility(age, occupation, land_acres)**
  Calculates eligibility for schemes such as Rythu Bandhu or pensions.

* **get_scheme_details(scheme_name)**
  Returns official details, benefits, and deadlines for a scheme.

---

## 6. Failure Handling Strategy

The system includes robust recovery mechanisms:

### 1. Transcription Errors

* **Issue:** STT returns gibberish or empty output
* **Recovery:** Agent politely asks the user to repeat the input in Telugu

### 2. Invalid or Impossible Inputs

* **Issue:** User provides unrealistic data (e.g., age = 200)
* **Recovery:** Tool validation errors are converted into polite corrections

---

## 7. Architectural Strengths

* Fully agentic decision-making (not rule-based chatbot)
* Voice-first Telugu-native interaction
* Clear separation of reasoning, tools, and synthesis
* Scalable architecture using LangGraph

---

## 8. Limitations & Future Enhancements

* Add persistent long-term memory (database-backed)
* Support dialectal Telugu variations
* Enable multimodal input (text + voice)
* Integrate official government databases

---

**End of Architecture Document**

