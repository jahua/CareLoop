import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatTime(timestamp: string) {
  return new Date(timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
}

export function formatDate(timestamp: string) {
  return new Date(timestamp).toLocaleDateString([], {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

export function getPersonalityColor(trait: string, value: number, confidence: number) {
  if (confidence < 0.6) return 'bg-gray-200';
  
  const colorMap = {
    'O': value > 0 ? 'bg-purple-500' : 'bg-purple-300',
    'C': value > 0 ? 'bg-blue-500' : 'bg-blue-300', 
    'E': value > 0 ? 'bg-green-500' : 'bg-green-300',
    'A': value > 0 ? 'bg-yellow-500' : 'bg-yellow-300',
    'N': value > 0 ? 'bg-red-300' : 'bg-red-500', // Inverted for neuroticism
  };
  
  return colorMap[trait as keyof typeof colorMap] || 'bg-gray-400';
}

export function getConfidenceText(confidence: number) {
  if (confidence >= 0.9) return 'Very High';
  if (confidence >= 0.7) return 'High';
  if (confidence >= 0.5) return 'Medium';
  if (confidence >= 0.3) return 'Low';
  return 'Very Low';
}

export function normalizePersonalityValue(value: number) {
  // Convert from [-1, 1] to [0, 100] for display
  return ((value + 1) / 2) * 100;
}

export function truncateText(text: string, maxLength: number) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}
