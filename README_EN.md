<a name="readme-top"></a>

<!-- TODO -->

[![Info][forks-shield]][forks-url]
[![Apache License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://airyuan.cn/home">
    <img src="docs/images/favicon.png" alt="Logo" width="400" height="160">
  </a>

  <p align="center">
    Open Source Yuan LLM Chat Application
    <br />
    <a href="https://airyuan.cn/home"><strong>Yuan Home Page »</strong></a>
    <br />
    <br />
  </p>

English / [简体中文](./README.md)

</div>

## :tada: 最近更新
* :fire: [2024-02-04] [**推出 Windows 桌面版 YuanChat.exe** :point_right:](./docs/推出Windows桌面版YuanChat.exe.md)
* :fire: [2024-01-05] [**笔记本上快速部署Yuan大模型和YuanChat** :point_right:](./docs/在笔记本上快速部署YuanModel和YuanChat.md)
---

<!-- TODO -->
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#1-deploy-with-docker">Deploy with Docker</a></li>
        <li><a href="#2-deploy-with-source">Deploy with source</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>

  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

<!-- TODO -->

![YuanChat Screen Shot][product-screenshotgif]

`YuanChat` is a part of [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main) project, it is a client side application for [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main). `YuanChat` provides an easy way to make users communicate with [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main), users can easily test and use [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main) LLM models.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

Thanks for these awesome projects:

[![FastAPI][FastAPI.com]][FastAPI-url][![Vue][Vue.js]][Vue-url][![NodeJS][nodejs.org]][Nodejs-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### 1. Deploy with Docker

#### 1.1 Prerequisites

Before deploy with docker, you need to install:

- [Docker](https://www.docker.com/) 18.03+
- [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main), deploy docker [instruction](https://github.com/IEIT-Yuan/Yuan-2.0/blob/main/README-EN.md#quick-start), run inference get model request url `http://127.0.0.1:8000` [instruction](https://github.com/IEIT-Yuan/Yuan-2.0/blob/main/docs/inference_server.md)
- [Chrome](https://www.google.com/chrome)

#### 1.2 Deploy

We provide a prebuilt image for `YuanChat`, you can directly deploy this project with one command.

<!-- TODO -->

```shell
docker run --rm -d --name yuanchat -p 5050:5050 -e YUAN_2_URL=http://ip:port/yuan yuanmodel/yuanchat:latest
```

Here, `YUAN_2_URL=http://ip:port/yuan` is the url of [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main) model server, ip is the ip address of your [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main) server,
and the port is the server port. eg. `http://192.168.1.1:8000/yuan`.

#### 1.3 Verify

Open link [http://localhost:5050](http://localhost:5050) in browser , if everything ok, you will see this page:

![YuanChat Screen Shot][product-screenshot]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

### 2. Deploy with source

<!-- TODO -->

**Build and deploy your own version with source code.**

#### 2.1 Prerequisites

Before deploy with source code, you need to setup development environment:

- [Python](https://www.python.org/downloads/) 3.8+
- [nodejs](https://nodejs.org/) 18+
- [Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main), deploy docker [instruction](https://github.com/IEIT-Yuan/Yuan-2.0/blob/main/README-EN.md#quick-start), run inference get model request url http://127.0.0.1:8000
- [Chrome](https://www.google.com/chrome)

#### 2.2 Deploy

##### 2.2.1 Download source code

```shell
git clone https://github.com/IEIT-Yuan/YuanChat.git
```

##### 2.2.2 Generate static files

```shell
cd YuanChat/src/webui
npm install
npm run build
```

> _For more webui details, please read the webui [README](src/webui/README_EN.md)_

##### 2.2.3 Modify project config file

If your `Yuan-2.0` model server address is not `http://127.0.0.1:8000`, you need to specify the to the right server address in `YuanChat/src/python/yuan_processing/as_constants.py` for param `YUAN_2_URL`,
such as `YUAN_2_URL=http://192.168.1.1:8000/yuan`

> _For more python server details, please read the python server [README](src/python/README_EN.md)_

##### 2.2.4 Install python packages

```shell
cd YuanChat
pip install -r requirements.txt
```

<!-- ##### 2.2.6 Download `roberta.ckpt` file
Because the limitation of `github`, we can not upload file `roberta.ckpt` to this repo, so you need to download [reberta.ckpt](https://huggingface.co/lilianlhl/roberta_intent_cls/tree/main), and put the file in dir:`YuanChat/src/python/yuan_processing/saved_dict/` -->

##### 2.2.5 Start python server

```shell
cd YuanChat
bash start.sh
```

#### 2.2.6 Web UI customization

- To modify the logo in the upper left corner of the Yuan Chat Web UI, you need replace `/src/webui/public/logo.png` with a pre prepared logo image. It is recommended that the image size be 120 \* 48.

- To modify the welcome message for the conversation in the Yuan Chat, you need modify the language configuration in `/src/webui/src/locales/lang/en.js` . Specifically, the following content needs to be modified:

```javascript
   welcomeHeader: 'I am YuanChat, a dialogue application based on Yuan 2.0 large language model.',
  welcomeParagraph1:'I am capable of engaging in multi-turn conversations, answering domain-specific questions, and assisting individuals in application writing and artistic creation.',
```

- To modify the recommended questions of the Yuan Chat, you need modify the content in `/src/webui/public/recommends.json` .

When you are in the local development mode of the web UI (please refer to [README](src/webui/README_EN.md)), the above modifications will take effect immediately. If you want to deploy, please refer to [Deploy with source](#222-generate-static-files)

#### 2.3 Verify

Open link [http://localhost:5050](http://localhost:5050) in browser , if everything ok, you will see this page:

![YuanChat Screen Shot][product-screenshot]

<!-- ROADMAP -->

## Roadmap

- [ ] Add README_zh.md

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

<!-- TODO -->

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

<!-- TODO -->

Distributed under the `YuanChat License`. See [YuanChat LICENSE](./LICENSE-YuanChat) file for more information.
<br />
Distributed under the `Apache License 2.0`. See [LICENSE](./LICENSE) file for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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
