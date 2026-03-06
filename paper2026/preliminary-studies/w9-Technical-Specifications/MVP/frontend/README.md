# Phase 1 Enhanced Personality AI Frontend

## Overview

This is a NextChat-inspired frontend for the Phase 1 Enhanced Personality-Adaptive Chatbot System. It features multi-agent visualization, real-time EMA smoothing monitoring, and advanced personality analytics.

## 🚀 Features

### Core Features
- **NextChat-Inspired UI**: Modern, responsive chat interface with smooth animations
- **Multi-Agent Dashboard**: Real-time monitoring of agent activities and performance
- **Enhanced Personality Visualization**: Interactive OCEAN trait analysis with EMA smoothing indicators
- **Real-time Updates**: Live agent status, personality state changes, and verification scores
- **Mobile Responsive**: Optimized for all screen sizes

### Phase 1 Enhancements
- **EMA Smoothing Visualization**: Watch personality traits stabilize over time
- **Verification Pipeline Monitoring**: See response quality scores and refinement actions
- **Agent Coordination Tracking**: Monitor how agents work together in the pipeline
- **Session Persistence**: Maintain conversation state across sessions
- **Advanced Analytics**: Personality evolution charts and confidence scoring

## 🛠 Technology Stack

- **Framework**: Next.js 14 with App Router
- **State Management**: Zustand for global state
- **UI Components**: Custom components with Tailwind CSS
- **Animations**: Framer Motion for smooth interactions
- **Charts**: Recharts for personality visualization
- **Notifications**: React Hot Toast for user feedback
- **TypeScript**: Full type safety throughout

## 📦 Dependencies

### Core Dependencies
- `next`: Next.js framework
- `react`: React library
- `react-dom`: React DOM renderer
- `typescript`: TypeScript support

### Enhanced Features
- `framer-motion`: Smooth animations and transitions
- `recharts`: Interactive charts for personality data
- `zustand`: Lightweight state management
- `react-hot-toast`: User notifications
- `lucide-react`: Modern icon set
- `tailwind-merge`: Utility for merging Tailwind classes
- `class-variance-authority`: Component variant management
- `clsx`: Conditional class names

### Utilities
- `axios`: HTTP client for API calls
- `uuid`: Unique identifier generation
- `date-fns`: Date manipulation utilities
- `react-use`: Collection of React hooks

## 🚦 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Phase 1 API server running on port 3001
- N8N workflow system on port 5678

### Installation

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Set up environment variables**:
```bash
cp env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_N8N_WEBHOOK_URL=http://localhost:5678/webhook
NODE_ENV=development
```

3. **Run development server**:
```bash
npm run dev
```

4. **Open in browser**:
Visit [http://localhost:3000](http://localhost:3000)

### Production Build

```bash
npm run build
npm start
```

### Docker Deployment

```bash
docker build -t personality-ai-frontend .
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:3001 \
  -e NEXT_PUBLIC_N8N_WEBHOOK_URL=http://localhost:5678/webhook \
  personality-ai-frontend
```

## 🎨 UI Components

### Main Components

- **EnhancedChatInterface**: Modern chat with personality adaptation indicators
- **EnhancedPersonalityDashboard**: Advanced OCEAN trait visualization with EMA monitoring
- **MultiAgentDashboard**: Real-time agent activity and performance monitoring

### Utility Components

- **Personality State Visualization**: Interactive trait bars with confidence indicators
- **Agent Status Cards**: Individual agent monitoring with capability lists
- **EMA Smoothing Indicators**: Visual representation of personality stabilization
- **Verification Pipeline Tracking**: Response quality and refinement monitoring

## 🔧 Configuration

### Environment Variables

```env
# Required
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_N8N_WEBHOOK_URL=http://localhost:5678/webhook

# Optional Feature Flags
NEXT_PUBLIC_ENABLE_ADVANCED_PERSONALITY=true
NEXT_PUBLIC_ENABLE_MULTI_AGENT_VIEW=true
NEXT_PUBLIC_ENABLE_EMA_VISUALIZATION=true
NEXT_PUBLIC_ENABLE_REAL_TIME_UPDATES=true

# UI Configuration
NEXT_PUBLIC_THEME=light
NEXT_PUBLIC_DEFAULT_VIEW=chat
NEXT_PUBLIC_ENABLE_ANIMATIONS=true
```

### API Integration

The frontend integrates with:

1. **Phase 1 API Server** (port 3001):
   - `/api/chat/message` - Send messages and receive personality-adapted responses
   - `/api/chat/session/{id}` - Retrieve session history
   - `/api/health` - System health monitoring

2. **N8N Webhook System** (port 5678):
   - `/webhook/chat` - Direct N8N workflow integration (fallback)
   - `/webhook/test` - Connection testing

## 📊 Multi-Agent Features

### Agent Types

1. **Personality Detection Agent**
   - OCEAN trait detection
   - EMA smoothing application
   - Confidence scoring

2. **Behavioral Regulation Agent**
   - Directive mapping
   - Therapeutic guideline application
   - Personality-appropriate strategy selection

3. **Response Generation Agent**
   - Personality-aware response creation
   - Therapeutic communication
   - Contextual adaptation

4. **Quality Verification Agent**
   - Response quality assessment
   - Directive adherence checking
   - Automatic refinement triggering

5. **Session Coordination Agent**
   - Multi-agent orchestration
   - Session state management
   - Crisis detection and escalation

### Real-time Monitoring

- **Agent Status**: Active, idle, processing, error states
- **Activity Timeline**: Recent agent actions with success/failure indicators
- **Performance Metrics**: Success rates, processing times, total actions
- **Capability Tracking**: What each agent can do and when it's used

## 🧠 Personality Features

### OCEAN Trait Visualization

- **Interactive Trait Cards**: Click to expand detailed information
- **Confidence Indicators**: Visual representation of detection certainty
- **EMA Smoothing Display**: See raw vs. smoothed personality values
- **Stability Tracking**: Monitor when personality profile becomes stable

### Advanced Analytics

- **Radar Charts**: Multi-dimensional personality visualization
- **Confidence Evolution**: Track how certainty improves over time
- **Adaptation Strategy Display**: Current therapeutic directives
- **Session Progress**: Personality detection progress indicators

## 🔄 State Management

### Zustand Store Structure

```typescript
interface PersonalityStore {
  // Session Management
  sessionId: string;
  messages: Message[];
  personalityState: PersonalityState;
  
  // Agent Management
  agents: Agent[];
  agentActivities: AgentActivity[];
  
  // System State
  isLoading: boolean;
  connectionStatus: 'connecting' | 'connected' | 'error';
  systemHealth: SystemHealth | null;
  
  // Actions
  sendMessage: (content: string) => Promise<void>;
  updatePersonalityState: (state: Partial<PersonalityState>) => void;
  updateAgentStatus: (agentId: string, status: Agent['status']) => void;
  // ... more actions
}
```

## 🎯 NextChat Integration

### Inspired Features

- **Clean Modern UI**: Minimalist design with focus on conversation
- **Smooth Animations**: Framer Motion for polished interactions
- **Responsive Layout**: Mobile-first responsive design
- **Message Actions**: Copy, retry, and other message interactions
- **Typing Indicators**: Visual feedback during AI processing
- **Connection Status**: Real-time connection monitoring

### Enhanced Beyond NextChat

- **Multi-Agent Visualization**: Unique agent monitoring capabilities
- **Personality Analytics**: Advanced psychological trait tracking
- **EMA Smoothing Monitoring**: Real-time personality stabilization
- **Therapeutic Adaptation**: Clinical-grade response verification
- **Session Persistence**: Conversation continuity across sessions

## 🚀 Development

### Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js app router pages
│   ├── components/          # React components
│   │   ├── EnhancedChatInterface.tsx
│   │   ├── EnhancedPersonalityDashboard.tsx
│   │   └── MultiAgentDashboard.tsx
│   ├── lib/                 # Utility functions
│   ├── store/               # Zustand state management
│   └── types/               # TypeScript type definitions
├── public/                  # Static assets
├── package.json             # Dependencies and scripts
├── next.config.js           # Next.js configuration
├── tailwind.config.js       # Tailwind CSS configuration
└── Dockerfile               # Container configuration
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler

## 📈 Performance

### Optimizations

- **Code Splitting**: Automatic route-based code splitting
- **Image Optimization**: Next.js automatic image optimization
- **Bundle Analysis**: Built-in bundle analyzer
- **Server-Side Rendering**: SSR for better performance
- **Static Generation**: Pre-generated static pages where possible

### Monitoring

- **Real-time Performance**: Agent processing times
- **Connection Health**: API and N8N connectivity status
- **Memory Usage**: Client-side state management efficiency
- **Load Times**: Page and component loading metrics

## 🔧 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check if Phase 1 API server is running on port 3001
   - Verify `NEXT_PUBLIC_API_URL` environment variable

2. **N8N Connection Issues**
   - Ensure N8N is running on port 5678
   - Check `NEXT_PUBLIC_N8N_WEBHOOK_URL` configuration

3. **Agent Status Not Updating**
   - Verify WebSocket connections (if implemented)
   - Check browser console for JavaScript errors

4. **Personality Data Not Displaying**
   - Ensure API responses include personality_state field
   - Check Zustand store state in browser dev tools

### Debug Mode

Enable debug mode with:
```env
NEXT_PUBLIC_DEBUG_MODE=true
```

This will:
- Enable console logging
- Show additional UI debug information
- Display API request/response details
- Show agent activity in detail

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is part of the Phase 1 Enhanced Personality-Adaptive Chatbot System and follows the same licensing terms.
