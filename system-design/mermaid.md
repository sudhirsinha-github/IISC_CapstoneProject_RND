

```js

classDiagram
    class RouterAgent {
        - llm: BaseLLM
        - name: str
        + run(state: ConversationState): ConversationState
        + route_intent(state): str
    }
    class Agent {
        <<abstract>>
        - name: str
        - llm: BaseLLM
        + run(input_text: str): str
    }
    class BaseLLM {
        <<interface>>
        + generate(prompt: str): str
    }
    class ConversationState {
        + user_message: str
        + agent_response: str
        + context: dict
    }

    RouterAgent --|> Agent
    RouterAgent --> BaseLLM
    RouterAgent --> ConversationState

```


```js
lassDiagram
    class BookingAgent {
        - llm: BaseLLM
        - name: str
        + run(state: ConversationState): ConversationState
        + extract_booking_details(state): dict
    }
    class Agent {
        <<abstract>>
        - name: str
        - llm: BaseLLM
        + run(input_text: str): str
    }
    class BaseLLM {
        <<interface>>
        + generate(prompt: str): str
    }
    class ConversationState {
        + user_message: str
        + agent_response: str
        + context: dict
    }

    BookingAgent --|> Agent
    BookingAgent --> BaseLLM
    BookingAgent --> ConversationState

```

``` js
classDiagram
    class FlightStatusAgent {
        - llm: BaseLLM
        - name: str
        + run(state: ConversationState): ConversationState
        + fetch_flight_status(state): dict
    }
    class Agent {
        <<abstract>>
        - name: str
        - llm: BaseLLM
        + run(input_text: str): str
    }
    class BaseLLM {
        <<interface>>
        + generate(prompt: str): str
    }
    class ConversationState {
        + user_message: str
        + agent_response: str
        + context: dict
    }

    FlightStatusAgent --|> Agent
    FlightStatusAgent --> BaseLLM
    FlightStatusAgent --> ConversationState

```

```js
classDiagram
    class BaggageAgent {
        - llm: BaseLLM
        - name: str
        + run(state: ConversationState): ConversationState
        + handle_baggage_query(state): dict
    }
    class Agent {
        <<abstract>>
        - name: str
        - llm: BaseLLM
        + run(input_text: str): str
    }
    class BaseLLM {
        <<interface>>
        + generate(prompt: str): str
    }
    class ConversationState {
        + user_message: str
        + agent_response: str
        + context: dict
    }

    BaggageAgent --|> Agent
    BaggageAgent --> BaseLLM
    BaggageAgent --> ConversationState

```

```js
sequenceDiagram
    participant User
    participant UI as Frontend/UI
    participant API as FastAPI (api/chat.py)
    participant Router as RouterAgent
    participant Booking as BookingAgent
    participant Flight as FlightStatusAgent
    participant Baggage as BaggageAgent
    participant State as ConversationState
    participant LLM as LLM (llama-cpp-python)
    participant Prompts as Prompts/Config

    User->>UI: Enter message
    UI->>API: POST /chat (user message)
    API->>State: Create/Update ConversationState
    API->>Router: run(state)
    Router->>Prompts: Load router_prompt.txt
    Router->>LLM: generate(router prompt + user message)
    LLM-->>Router: Classification (intent, sentiment, topic) + reply
    Router->>State: Update state with intent, reply
    alt intent == "booking"
        Router->>Booking: run(state)
        Booking->>Prompts: Load booking prompt
        Booking->>LLM: generate(booking prompt + user message)
        LLM-->>Booking: Booking response
        Booking->>State: Update agent_response
    else intent == "flight_status"
        Router->>Flight: run(state)
        Flight->>Prompts: Load flight status prompt
        Flight->>LLM: generate(flight status prompt + user message)
        LLM-->>Flight: Flight status response
        Flight->>State: Update agent_response
    else intent == "baggage"
        Router->>Baggage: run(state)
        Baggage->>Prompts: Load baggage prompt
        Baggage->>LLM: generate(baggage prompt + user message)
        LLM-->>Baggage: Baggage response
        Baggage->>State: Update agent_response
    else intent == "generic_query" or "out_of_scope"
        Router->>State: Use router's reply as agent_response
    end
    API->>UI: Return agent_response
    UI->>User: Display response

```

```js
%% Component Diagram for Agentic Chatbot Project
flowchart TD
    subgraph Frontend
        UI["React UI (ui/src)"]
    end

    subgraph API
        FastAPI["FastAPI Server (api/chat.py)"]
    end

    subgraph Agentic_Core["Agentic Core (src/ai_agent)"]
        RouterAgent["RouterAgent"]
        BookingAgent["BookingAgent"]
        FlightStatusAgent["FlightStatusAgent"]
        BaggageAgent["BaggageAgent"]
        ConversationState["ConversationState"]
        AgentGraph["AgentGraph / GraphBuilder"]
        Prompts["Prompts (prompts/)"]
        Config["Config (configs/)"]
        Utils["Utils (utils/)"]
    end

    subgraph LLM_and_DB["LLM & Vector DB"]
        LLM["LLM (llama-cpp-python, Mistral)"]
        VectorDB["Vector DB (faiss-cpu)"]
    end

    %% Connections
    UI -- "REST API\n(user message)" --> FastAPI
    FastAPI -- "Invoke agentic core" --> RouterAgent
    RouterAgent -- "Intent routing" --> BookingAgent
    RouterAgent -- "Intent routing" --> FlightStatusAgent
    RouterAgent -- "Intent routing" --> BaggageAgent
    RouterAgent -- "State mgmt" --> ConversationState
    RouterAgent -- "Prompt loading" --> Prompts
    RouterAgent -- "Config" --> Config
    RouterAgent -- "Utils" --> Utils
    RouterAgent -- "Graph orchestration" --> AgentGraph

    BookingAgent -- "State mgmt" --> ConversationState
    BookingAgent -- "Prompt loading" --> Prompts
    BookingAgent -- "LLM call" --> LLM
    BookingAgent -- "Vector search" --> VectorDB

    FlightStatusAgent -- "State mgmt" --> ConversationState
    FlightStatusAgent -- "Prompt loading" --> Prompts
    FlightStatusAgent -- "LLM call" --> LLM

    BaggageAgent -- "State mgmt" --> ConversationState
    BaggageAgent -- "Prompt loading" --> Prompts
    BaggageAgent -- "LLM call" --> LLM

    AgentGraph -- "Orchestrates" --> BookingAgent
    AgentGraph -- "Orchestrates" --> FlightStatusAgent
    AgentGraph -- "Orchestrates" --> BaggageAgent

    FastAPI -- "Returns response" --> UI

```


```js
stateDiagram-v2
    [*] --> Idle

    Idle --> ReceivingUserMessage: User sends message

    ReceivingUserMessage --> ClassifyingIntent: API creates/updates ConversationState

    ClassifyingIntent --> Routing: RouterAgent classifies intent

    Routing --> BookingFlow: intent == "booking"
    Routing --> FlightStatusFlow: intent == "flight_status"
    Routing --> BaggageFlow: intent == "baggage"
    Routing --> GenericFlow: intent == "generic_query" or "out_of_scope"

    BookingFlow --> GeneratingResponse: BookingAgent generates response
    FlightStatusFlow --> GeneratingResponse: FlightStatusAgent generates response
    BaggageFlow --> GeneratingResponse: BaggageAgent generates response
    GenericFlow --> GeneratingResponse: RouterAgent generates generic response

    GeneratingResponse --> SendingResponse: Update ConversationState with agent_response

    SendingResponse --> Idle: Response sent to user

    note right of ClassifyingIntent
      Loads router prompt
      Calls LLM for intent/sentiment/topic
      Updates state
    end note

    note right of GeneratingResponse
      Loads agent-specific prompt
      Calls LLM for reply
      Updates state
    end note


```


