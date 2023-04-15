export default {
  testEnvironment: 'jest-environment-jsdom',
  transform: {
    '^.+\\.js$': 'babel-jest',
  },
  setupFiles: ['jest-canvas-mock'],
  setupFilesAfterEnv: ['./jest.setup.js'],
};