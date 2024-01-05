<a name="readme-top"></a>

<!-- TODO -->

[![Info][forks-shield]][forks-url]
[![Apache License][license-shield]][license-url]

<!-- 项目LOGO -->
<br />
<div align="center">
  <a href="https://airyuan.cn/home">
    <img src="docs/images/favicon.png" alt="Logo" width="400" height="160">
  </a>

  <p align="center">
    Yuan LLM 开源项目对话应用
    <br />
    <a href="https://airyuan.cn/home"><strong> 源官网 »</strong></a>
    <br />
    <br />
  </p>

[English](./README_EN.md) / 简体中文

</div>

## :tada: 最近更新
* :fire: **在笔记本上快速部署Yuan大模型和YuanChat** [:point_right:](./docs/在笔记本上快速部署YuanModel和YuanChat.md)

<!-- TODO -->
<!-- TABLE OF CONTENTS -->
<details>
  <summary>目录</summary>
  <ol>
    <li>
      <a href="#about-the-project">关于</a>
      <ul>
        <li><a href="#built-with">构建</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">开始</a>
      <ul>
        <li><a href="#1-deploy-with-docker">Docker部署</a></li>
        <li><a href="#2-deploy-with-source">源码部署</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">产品规划</a></li>
    <li><a href="#contributing">贡献</a></li>
    <li><a href="#license">许可</a></li>

  </ol>
</details>

<!-- 关于 -->

## 关于

<!-- TODO -->

![YuanChat Screen Shot][product-screenshotgif]

`源Chat` 是[Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main) 项目的一部分, 作为[Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main)的一个客户端应用. `源Chat` 提供了一种简单的交互方式，可以让用户很轻松的使用 [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main), 用户可以很方便的进行测试以及使用。

<p align="right">(<a href="#readme-top">回到顶端</a>)</p>

### 构建

本项目基于下面这些优秀的项目：

[![FastAPI][FastAPI.com]][FastAPI-url][![Vue][Vue.js]][Vue-url][![NodeJS][nodejs.org]][Nodejs-url]

<p align="right">(<a href="#readme-top">回到顶端</a>)</p>

<!-- GETTING STARTED -->

## 开始

### 1. Docker 部署

#### 1.1 依赖条件

首先，在您使用 Docker 部署之前，您需要先安装：

- [Docker](https://www.docker.com/) 18.03+
- [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main), 部署 Docker [参考](https://github.com/IEIT-Yuan/Yuan-2.0/blob/main/README.md#%E5%BF%AB%E9%80%9F%E5%90%AF%E5%8A%A8), 获取推理服务的 request url：`http://127.0.0.1:8000` [参考](https://github.com/IEIT-Yuan/Yuan-2.0/blob/main/docs/inference_server_cn.md)
- [Chrome](https://www.google.com/chrome)

#### 1.2 部署

我们提供了一个制作好的`源Chat`镜像，一条命令就可以完成项目的部署操作。

<!-- TODO -->

```shell
docker run --rm -d --name yuanchat -p 5050:5050 -e YUAN_2_URL=http://ip:port/yuan yuanmodel/yuanchat:latest
```

这里， `YUAN_2_URL=http://ip:port/yuan` 是[Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main)模型服务的地址，ip 是你部署[Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main)服务的节点 ip，port 是服务对外端口，例如，你可以这样写：`http://192.168.1.1:8000/yuan` 。

#### 1.3 验证

在浏览器中访问链接：[http://localhost:5050](http://localhost:5050)，如果部署正确，那么你将会看到这个页面：

![YuanChat Screen Shot][product-screenshot]

<p align="right">(<a href="#readme-top">回到顶端</a>)</p>

---

### 2. 源码部署

<!-- TODO -->

**用源码创建并部署属于你自己的版本**

#### 2.1 依赖条件

在源码部署之前，你需要安装以下开发环境

- [Pyhton](https://www.python.org/downloads/) 3.8+
- [nodejs](https://nodejs.org/) 18+
- [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main), 部署 Docker [参考](https://github.com/IEIT-Yuan/Yuan-2.0/blob/main/README.md#%E5%BF%AB%E9%80%9F%E5%90%AF%E5%8A%A8), 获取推理服务的 request url：`http://127.0.0.1:8000` [参考](https://github.com/IEIT-Yuan/Yuan-2.0/blob/main/docs/inference_server_cn.md)
- [Chrome](https://www.google.com/chrome)

#### 2.2 部署

##### 2.2.1 下载源码

```shell
git clone https://github.com/IEIT-Yuan/YuanChat.git
```

##### 2.2.2 生成静态文件

```shell
cd YuanChat/src/webui
npm install
npm run build
```

> _获取更多 webui 详细信息，请参考 [README](src/webui/README.md)_

##### 2.2.3 修改项目配置文件

如果你的`Yuan-2.0` 模型服务的地址不是`http://127.0.0.1:8000`，你需要在`YuanChat/src/python/yuan_processing/as_constants.py`中`YUAN_2_URL`参数指定正确的地址，例如：`YUAN_2_URL=http://192.168.1.1:8000/yuan`

> _获取更多 python 服务端详细信息，请参考 [README](src/python/README.md)_

##### 2.2.4 安装 python 依赖包

```shell
cd YuanChat
pip install -r requirements.txt
```

##### 2.2.5 启动 python 服务

```shell
cd YuanChat
bash start.sh
```

#### 2.2.6 Web UI 定制修改

- 修改源 Chat Web UI 左上角的 Logo，需要将 `/src/webui/public/logo.png` 替换为提前准备好的 Logo 图片，建议图片尺寸为 120\*48。

- 修改源 Chat 的对话欢迎语，需要修改 `/src/webui/src/locales/lang/zh-CN.js` 中的多语言配置，具体要修改以下内容：

```javascript
  welcomeHeader: '我是源Chat，基于源2.0大模型的对话应用。',
  welcomeParagraph1: '我能够进行多轮对话，回答领域问题，协助人们进行应用文写作和艺术创作。',
```

- 修改源 Chat 的对话推荐问题，需要修改 `/src/webui/public/recommends.json` 中的内容。

当你处于 web UI 的本地开发模式（请参考 [README](src/webui/README.md)），以上修改将立即生效。如果要部署，请参考[源码部署](#222-生成静态文件)章节

#### 2.3 验证

在浏览器中访问链接 [http://localhost:5050](http://localhost:5050)，如果部署正确，那么你将会看到这个页面：

![YuanChat Screen Shot][product-screenshot]

<!-- ROADMAP -->

## 产品规划

- [x] 增加 README 中文文档
- [ ] 增加 windows+GPU 部署说明

<p align="right">(<a href="#readme-top">回到顶端</a>)</p>

<!-- CONTRIBUTING -->

## 贡献

<!-- TODO -->

贡献使得开源社区成为一个学习、激励和创造的绝佳场所。**非常感谢**您的任何贡献。

如果你对我们有更好的建议，请将仓库 fork 下来，并创建一个 pr。您也可以简单点，用标签“优化”给我们提一个问题。
别忘了给这个项目打一颗星！再次感谢！

1. 从仓库 Fork 项目
2. 创建一个你的分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的变更 (`git commit -m 'Add some AmazingFeature'`)
4. 将代码 push 到你的远程分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

<p align="right">(<a href="#readme-top">回到顶端</a>)</p>

<!-- LICENSE -->

## 许可

<!-- TODO -->

在`YuanChat License`下分发. 获取更多信息请参考 [YuanChat LICENSE](./LICENSE-YuanChat) .
<br />
在`Apache License 2.0`下分发. 获取更多信息请参考 [LICENSE](./LICENSE) .

<p align="right">(<a href="#readme-top">回到顶端</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/stars/ieit-yuan?label=IEIT-Yuan%20Stars
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/badge/IEIT_Yuan-Open_Source-blue?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/badge/license-apache20-green?style=for-the-badge
[license-url]: ./LISENCE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: docs/images/screenshot.jpg
[product-screenshotgif]: docs/images/screenshot.gif
[FastAPI.com]: https://img.shields.io/badge/fastapi-white?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[nodejs.org]: https://img.shields.io/badge/nodejs-white?style=for-the-badge&logo=node.js
[Nodejs-url]: https://nodejs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
