FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the evaluation scripts and related files
COPY multi_agent_ocean.py quick_llama31_5shot_eval.py benchmark_llama31_prompt_tuning.py ./
COPY MULTI-AGENT-README.md README.md ./

# Create results directory
RUN mkdir -p results

# Make scripts executable
RUN chmod +x *.py

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV NVIDIA_API_KEY=${NVIDIA_API_KEY:-""}
ENV NVIDIA_API_URL=https://integrate.api.nvidia.com/v1/chat/completions

# Default command shows help
CMD ["echo", "🚀 Big5Loop Multi-Agent Docker Ready! Use: docker exec -it big5loop-multi-agent python3 multi_agent_ocean.py --dry-run --limit 5"]