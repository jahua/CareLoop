/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@careloop/contracts"],
};

module.exports = nextConfig;
