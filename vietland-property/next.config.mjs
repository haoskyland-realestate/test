/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Disabled so the build never needs to reach fonts.googleapis.com itself;
  // the Google Fonts <link> tags in app/layout.tsx still load normally in the browser.
  optimizeFonts: false,
};

export default nextConfig;
