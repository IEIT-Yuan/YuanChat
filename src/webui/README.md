<div align="center">

# 源Chat 网页交互应用

[English](./README_EN.md) / 简体中文

</div>

## 部署

请先确保已安装Node.js ( >=18 ).

### 1. 安装依赖

```sh
npm install
```

### 2. 编译代码

```sh
npm run build
```

## 本地开发

### 本地开发IDE推荐设置

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

### 1. 安装依赖

```sh
npm install
```

### 2. 配置 `vite.config.js`

```javascript
server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5050', // 将此处修改为你的后台服务地址
        secure: false,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
```

### 3. 启动本地服务

```sh
npm run dev
```
