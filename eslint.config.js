const js = require('@eslint/js');

module.exports = [
  {
    ignores: ['dist/', 'node_modules/', '.tox/', '.venv/'],
  },
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2019,
      sourceType: 'module',
      globals: {
        __dirname: 'readonly',
        console: 'readonly',
        exports: 'writable',
        module: 'readonly',
        require: 'readonly',
      },
    },
  },
];
