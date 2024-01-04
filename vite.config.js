const path = require('path');
const { defineConfig } = require('vite');

module.exports = defineConfig({
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
        fatalDeprecation: true,
      },
    },
  },
});
