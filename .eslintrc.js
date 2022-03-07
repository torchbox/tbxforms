module.exports = {
  extends: 'eslint:recommended',
  parserOptions: { ecmaVersion: 10, sourceType: 'module' },
  env: {
    browser: true,
    node: true,
  },
  ignorePatterns: ['dist/'],
};
