/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appRouter: true,
  },
  webpack: (config, { isServer }) => {
    // Fixes npm packages that need to be built with webpack still
    config.resolve.alias.fs = "fs";
    config.resolve.alias.tls = "tls";
    return config;
  },
};

module.exports = nextConfig;