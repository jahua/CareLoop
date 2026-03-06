# NextChat-Enhanced Installation Guide

## 🚀 Quick Start

Since we've created a simplified NextChat-Enhanced implementation, here are the manual installation steps:

### 1. Navigate to Directory

```bash
cd /Users/huaduojiejia/MyProject/hslu/2026/preliminary-studies/w9-Technical-Specifications/MVP/nextchat-personality-enhanced
```

### 2. Install Dependencies

```bash
# Using yarn (recommended)
yarn install

# Or using npm
npm install
```

### 3. Create Environment Configuration

```bash
# Copy the example environment file (if it exists)
cp .env.example .env.local

# Or create manually:
cat > .env.local << 'EOF'
# Phase 1 API Integration
PHASE1_API_URL=http://localhost:3001
N8N_URL=http://localhost:5678

# NextChat-Enhanced Features
ENABLE_PERSONALITY_ANALYTICS=true
ENABLE_MULTI_AGENT_MONITORING=true
ENABLE_EMA_VISUALIZATION=true
DEFAULT_PERSONALITY_MODE=true

# System Configuration
NEXTCHAT_PERSONALITY_VERSION=2.16.1-personality-v1.0
NODE_ENV=development

# Optional: OpenAI API Key (for fallback)
OPENAI_API_KEY=your-openai-key-here
EOF
```

### 4. Start Phase 1 Backend (Prerequisites)

Before running NextChat-Enhanced, make sure the Phase 1 backend is running:

```bash
# Navigate to Phase 1 directory
cd ../Phase-1

# Start all Phase 1 services
docker-compose up -d postgres redis n8n api-server

# Verify services are running
curl http://localhost:3001/api/health
curl http://localhost:5678
```

### 5. Run NextChat-Enhanced Development Server

```bash
# Go back to NextChat-Enhanced directory
cd ../nextchat-personality-enhanced

# Start development server
yarn dev

# Or with npm
npm run dev
```

### 6. Open in Browser

Open [http://localhost:3000](http://localhost:3000) to see NextChat-Enhanced!

---

## 🎯 What to Expect

When NextChat-Enhanced loads, you'll see:

### 1. **Main Interface**
- **Chat Tab**: Personality-adaptive conversation interface
- **Personality Tab**: Interactive OCEAN trait dashboard
- **Agents Tab**: Multi-agent system monitoring

### 2. **Personality Detection**
- Start chatting to see OCEAN traits appear
- Watch EMA smoothing stabilize personality over time
- View confidence scores and adaptation strategies

### 3. **Multi-Agent Coordination**
- See 5 agents working together:
  - 🧠 **Personality Detector**: OCEAN analysis + EMA smoothing
  - ⚙️ **Behavioral Regulator**: Therapeutic directive mapping
  - 💬 **Response Generator**: Personality-adapted responses
  - ✅ **Quality Verifier**: Response verification & refinement
  - 🎯 **Session Coordinator**: Multi-agent orchestration

### 4. **Real-Time Analytics**
- Personality evolution charts
- Agent performance metrics
- Verification quality scores
- System health monitoring

---

## 🔧 Troubleshooting

### Issue: "Phase 1 API not found"
**Solution**: Make sure Phase 1 backend is running on port 3001:
```bash
curl http://localhost:3001/api/health
```

### Issue: "Dependencies not installing"
**Solution**: Try using npm instead of yarn:
```bash
rm -rf node_modules package-lock.json yarn.lock
npm install
```

### Issue: "Port 3000 already in use"
**Solution**: Kill existing processes or use different port:
```bash
lsof -ti:3000 | xargs kill -9
# Or run on different port
yarn dev --port 3001
```

### Issue: "TypeScript errors"
**Solution**: Check types and run type checking:
```bash
yarn type-check
```

---

## 🎨 Features Active

- ✅ **NextChat-inspired UI** with personality enhancements
- ✅ **OCEAN Personality Detection** with EMA smoothing
- ✅ **Multi-Agent Coordination** (5 specialized agents)
- ✅ **Real-time Monitoring** dashboards
- ✅ **Quality Verification** pipeline
- ✅ **Therapeutic Adaptation** with live directives
- ✅ **Interactive Analytics** and insights
- ✅ **System Health** monitoring

---

## 📱 Test Scenarios

### 1. Basic Chat Test
1. Start a conversation: "Hi, how are you?"
2. Watch personality traits appear in Personality tab
3. Continue chatting to see EMA smoothing in action

### 2. Emotional Conversation Test
Use the emotional conversation from Phase 1 testing:
```
"I don't know… kind of all over the place, I guess. Everything just feels like too much lately, and I don't even know where to start or if it's worth talking about."
```

### 3. Agent Monitoring Test
1. Switch to Agents tab
2. Watch agents activate during conversation
3. Monitor performance metrics and activity timeline

---

## 🔗 System URLs

- **NextChat-Enhanced**: http://localhost:3000
- **Phase 1 API**: http://localhost:3001/api/health
- **N8N Workflow**: http://localhost:5678
- **PostgreSQL**: localhost:5432

---

Ready to experience **personality-adaptive AI** with NextChat's proven interface! 🚀

















































