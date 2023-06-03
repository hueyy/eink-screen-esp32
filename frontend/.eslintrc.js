module.exports = {
  env: {
    browser: true,
    es2021: true
  },
  extends: [
    'standard-with-typescript',
    'plugin:react-hooks/recommended'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: [
      './frontend/tsconfig.json'
    ]
  },
  rules: {
    '@typescript-eslint/explicit-function-return-type': 'off'
  }
}
