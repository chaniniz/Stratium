import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/prices': 'http://localhost:8000',
      '/token': 'http://localhost:8000',
      '/trade': 'http://localhost:8000',
      '/watchlist': 'http://localhost:8000'
    }
  }
});
