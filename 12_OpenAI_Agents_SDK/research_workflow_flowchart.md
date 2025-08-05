# Research Workflow Agent Interaction Flowchart

```mermaid
flowchart TD
    A[User Query] --> B[Planner Agent]
    B --> C{Generate Search Plan}
    C --> D[WebSearchPlan]
    D --> E[Search Agent]
    E --> F[WebSearchTool]
    F --> G[Search Results]
    G --> H[Writer Agent]
    H --> I[Final Report]
    
    B --> J[Structured Output:<br/>WebSearchPlan]
    E --> K[Tool Usage:<br/>WebSearchTool]
    H --> L[Structured Output:<br/>ReportData]
    
    subgraph "Agent Details"
        B1[Planner Agent<br/>Model: GPT-4.1<br/>Output: WebSearchPlan<br/>- reason<br/>- query]
        E1[Search Agent<br/>Model: GPT-4o<br/>Tool: WebSearchTool<br/>Output: Summaries]
        H1[Writer Agent<br/>Model: o3-mini<br/>Output: ReportData<br/>- short_summary<br/>- markdown_report<br/>- follow_up_questions]
    end
    
    B -.-> B1
    E -.-> E1
    H -.-> H1
    
    style A fill:#e1f5fe
    style I fill:#c8e6c9
    style B fill:#fff3e0
    style E fill:#fff3e0
    style H fill:#fff3e0
```

## Key Interactions:

1. **User Query** → **Planner Agent**: Generates structured search plan
2. **Planner Agent** → **Search Agent**: Provides search queries with reasoning
3. **Search Agent** → **WebSearchTool**: Executes web searches
4. **Search Agent** → **Writer Agent**: Provides summarized research results
5. **Writer Agent** → **Final Report**: Synthesizes comprehensive report

## Data Flow:
- **WebSearchPlan**: Contains list of search items with reason and query
- **Search Results**: Summarized findings from web searches
- **ReportData**: Structured final output with summary, report, and follow-up questions 