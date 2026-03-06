/** @type {import('next').NextConfig} */

const nextConfig = {
  experimental: {
    appDir: true,
    optimizeCss: false, // Disable to avoid critters dependency issue
  },
  
  // NextChat-Enhanced: Phase 1 Configuration
  env: {
    NEXTCHAT_PERSONALITY_VERSION: '2.16.1-personality-v1.0',
    PHASE1_ENABLED: 'true',
  },
  
  // API Configuration for Phase 1
  async rewrites() {
    const apiUrl = process.env.PHASE1_API_URL || 'http://localhost:3001';
    const webhookUrl = process.env.N8N_URL || 'http://localhost:5678';
    
    return [
      {
        source: '/api/phase1/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
      {
        source: '/api/n8n/:path*',
        destination: `${webhookUrl}/webhook/:path*`,
      },
    ];
  },
  
  // Build configuration
  output: process.env.BUILD_MODE === "export" ? "export" : undefined,
  images: {
    unoptimized: process.env.BUILD_MODE === "export",
  },
  trailingSlash: process.env.BUILD_MODE === "export",
  
  // NextChat optimizations
  reactStrictMode: false,
  swcMinify: true,
  productionBrowserSourceMaps: false,
  
  // Compiler optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' ? {
      exclude: ['error', 'warn'],
    } : false,
  },
  
  // Webpack configuration for NextChat patterns
  webpack: (config, { isServer }) => {
    config.module.rules.push({
      test: /\.svg$/,
      use: ["@svgr/webpack"],
    });
    
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }
    
    return config;
  },
  
  // Headers for CORS and security
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,OPTIONS,PATCH,DELETE,POST,PUT' },
          { key: 'Access-Control-Allow-Headers', value: 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization' },
        ],
      },
    ];
  },
};

export default nextConfig;

















































