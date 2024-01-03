<div align="center">

# Yuan Chat web UI

English / [简体中文](./README.md)

</div>

## Deploy

Please ensure that Node.js ( >=18 ) is installed.

### 1. Project Setup

```sh
npm install
```

### 2. Compile and Minify for Production

```sh
npm run build
```

## Local development

### Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

### 1. Project Setup

```sh
npm install
```

### 2. Customize configuration `vite.config.js`

```javascript
server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5050', // Change the target to your backend service address
        secure: false,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
```

### 3. Compile and Hot-Reload for Development

```sh
npm run dev
```
