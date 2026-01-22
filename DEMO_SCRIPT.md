# Demo Script & Example Queries

This document provides a guided walkthrough for demonstrating the Industrial AI Platform.

## Quick Demo (5 minutes)

### 1. Executive Dashboard Overview (2 min)

**What to show:**
- Navigate to Executive View
- Point out key metrics:
  - Total equipment count
  - Average health score
  - Active alerts
  - Maintenance costs

**Talking points:**
- "This gives leadership a real-time view of operational health"
- "The predicted failures use ML to forecast equipment issues before they occur"
- "Notice PUMP-007 has a 78% failure probability within 7 days"

### 2. Operator Dashboard (2 min)

**What to show:**
- Switch to Operator View
- Click on different equipment to show status
- Review active alerts

**Talking points:**
- "Operators see detailed equipment metrics in real-time"
- "Each piece of equipment shows temperature, pressure, vibration"
- "Color coding makes it easy to spot issues at a glance"

### 3. AI Assistant Demo (1 min)

**What to show:**
- Select "Hydraulic Pump 7" (the critical equipment)
- Ask: "What's causing the high vibration?"

**Expected behavior:**
- Multi-agent system routes through analysis and retrieval
- Returns answer with specific causes
- Provides actionable recommendations
- Shows documentation sources

**Talking points:**
- "The AI assistant combines multiple agents"
- "It analyzes real-time data AND searches maintenance manuals"
- "Gives operators immediate, expert-level guidance"

## Detailed Demo (15 minutes)

### Part 1: Executive Insights (5 min)

Start in Executive View.

**Scenario**: "Let's say you're the VP of Operations reviewing fleet health..."

1. **Overview Metrics**
   - "We have 5 pieces of equipment monitored"
   - "Overall health score is 73%, which is concerning"
   - "We have 2 unresolved alerts requiring attention"

2. **Predicted Failures**
   - "Our AI has flagged two pieces of equipment"
   - "PUMP-007 is the highest priority - 78% failure risk"
   - "The system tells us WHY - bearing degradation and high vibration"
   - "This gives us 7 days to plan maintenance, avoiding unplanned downtime"

3. **Cost Tracking**
   - "Month-to-date maintenance costs are tracked"
   - "Energy efficiency metrics help optimize operations"

### Part 2: Operator Workflow (5 min)

Switch to Operator View.

**Scenario**: "Now you're an equipment operator starting your shift..."

1. **Equipment Monitoring**
   - Click through different equipment
   - "Each piece shows live metrics"
   - "Green = good, Yellow = warning, Red = critical"

2. **Alert Response**
   - "You see a critical alert on PUMP-007"
   - "High vibration detected at 4.5 mm/s"
   - "This exceeds the safe threshold"

3. **Decision Support**
   - "Instead of calling maintenance or checking manuals..."
   - "Let's ask the AI assistant"

### Part 3: AI Assistant Deep Dive (5 min)

With PUMP-007 selected:

#### Query 1: Root Cause Analysis
**Ask**: "What's causing the high vibration in PUMP-007?"

**Expected response**:
- Analysis of vibration causes
- References to bearing wear and misalignment
- Citations from maintenance documentation
- Confidence score

**Talking points**:
- "The AI consulted maintenance manuals"
- "It's pulling from real technical documentation"
- "Notice the sources cited at the bottom"

#### Query 2: Procedure Lookup
**Ask**: "What's the procedure for replacing bearings?"

**Expected response**:
- Step-by-step bearing replacement procedure
- Safety precautions
- Required tools and parts
- Time estimates

**Talking points**:
- "The RAG pipeline searches all documentation"
- "It provides the exact procedure from the manual"
- "Operators get instant access to expertise"

#### Query 3: Recommendations
**Ask**: "What actions should I take right now?"

**Expected response**:
- Prioritized list of actions
- Immediate safety steps
- Maintenance scheduling recommendations
- Monitoring guidance

**Talking points**:
- "The recommendation agent synthesizes everything"
- "It considers current conditions, history, and best practices"
- "Operators get clear, actionable guidance"

## Example Queries by Category

### Equipment Status Questions

```
"What's the current status of all compressors?"
"Show me equipment with health scores below 70%"
"Which equipment is due for maintenance?"
"What are the operating parameters for TURB-003?"
```

### Troubleshooting Questions

```
"Why is the temperature high on COMP-001?"
"What causes vibration in hydraulic pumps?"
"The pressure is fluctuating on TURB-003, what should I check?"
"PUMP-007 is making unusual noise, what could it be?"
```

### Procedure Questions

```
"How do I perform a startup procedure for the gas turbine?"
"What's the maintenance schedule for air compressors?"
"Show me the shutdown procedure for HVAC-005"
"What are the safety precautions for bearing replacement?"
```

### Historical Questions

```
"Show me the maintenance history for PUMP-007"
"When was TURB-003 last serviced?"
"What repairs were done last month?"
"Have we had this issue before?"
```

### Predictive Questions

```
"Which equipment is most likely to fail?"
"When should I schedule preventive maintenance?"
"What are the warning signs of bearing failure?"
"How can I extend equipment lifespan?"
```

## Technical Deep Dive Demo

For technical audiences, highlight:

### 1. Multi-Agent Architecture
- Show code in `backend/app/agents/orchestrator.py`
- Explain the state graph approach
- Demonstrate agent routing logic

### 2. RAG Pipeline
- Show code in `backend/app/rag/pipeline.py`
- Explain document chunking and embedding
- Demonstrate vector similarity search

### 3. API Design
- Open http://localhost:8000/docs
- Show interactive API documentation
- Demonstrate endpoint testing

### 4. Frontend Architecture
- Show component structure
- Explain state management
- Demonstrate API integration

## Common Questions & Answers

**Q: "How accurate is the AI?"**
A: "The system provides confidence scores with each response. It's trained on real maintenance documentation and combines multiple data sources for accuracy."

**Q: "Can it work with our equipment?"**
A: "Yes, the platform is designed to be equipment-agnostic. You'd add your equipment specs and documentation to the system."

**Q: "What about data security?"**
A: "The system can be deployed on-premises. All sensitive data stays within your infrastructure."

**Q: "How does it learn?"**
A: "The RAG pipeline uses your documentation. As you add manuals and procedures, the system becomes more knowledgeable about your specific equipment."

**Q: "Does it replace technicians?"**
A: "No, it augments them. It gives technicians instant access to expertise and documentation, making them more effective."

## Performance Tips

For the best demo experience:

1. **Pre-load the page**: Have both dashboards loaded before demo
2. **Test queries first**: Make sure your OpenAI API is working
3. **Have backup queries**: In case one doesn't work well
4. **Know the data**: Understand which equipment has what issues
5. **Explain the value**: Connect features to business outcomes

## Customization for Different Audiences

### For Executives
- Focus on ROI and business metrics
- Highlight predicted failures and cost savings
- Show reporting and oversight capabilities

### For Operators
- Focus on ease of use and time savings
- Show practical troubleshooting scenarios
- Demonstrate procedure lookup

### For Technical Teams
- Show architecture and code
- Explain AI/ML approaches
- Discuss integration and customization

### For Safety/Compliance
- Show documentation tracking
- Demonstrate procedure adherence
- Highlight audit trail capabilities

## Metrics to Highlight

When demonstrating, emphasize these value propositions:

1. **Reduced Downtime**: Predictive maintenance prevents failures
2. **Faster Troubleshooting**: AI assistant provides instant guidance
3. **Knowledge Preservation**: Documentation accessible to all operators
4. **Improved Safety**: Proper procedures always available
5. **Better Decisions**: Data-driven insights for leadership

## Post-Demo Resources

Share with interested parties:
- GitHub repository link
- Setup guide (SETUP_GUIDE.md)
- Architecture documentation (ARCHITECTURE.md)
- README with project overview
- Your contact information
