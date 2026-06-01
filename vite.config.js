import path from 'path';
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    lib: {
      entry: path.resolve(__dirname, 'tbxforms/static/js/tbxforms.js'),
      name: 'TbxForms',
      fileName: (format) => `tbxforms.${format}.js`,
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern',
        fatalDeprecation: true,
      },
    },
  },
});
