# YuanChat V0.9.1 新版本功能优化升级

嗨，大家好，`YuanChat`近期进行了优化升级，升级版本V0.9.1，欢迎大家下载体验。

## 功能升级
* 优化模型列表
* PDF影印版支持
* 新增用户使用时长统计
* 修复已知问题

## 安装运行

您可以通过下载连接安装YuanChat进行体验，连接中包含`应用程序安装包`和`用户使用手册`。
**下载链接**：[阿里云盘](https://www.alipan.com/s/dfJrFSnUhkT)

## 模型列表优化
根据社区用户使用反馈，本次升级为更好满足社区用户硬件设备的限制，选取轻量化、小体积的模型，同一模型有不同的精度和量化版本，兼顾模型生成速度和准确率。
优化后的模型列表如下所示，您可以按需选择模型进行检索或对话：
<table>
    <tr>
        <td><b>模型</b></td> 
        <td><b>精度</b></td> 
   </tr>
   <tr>
        <td>Yuan2-2B-Mars-hf-GGUF</td> 
        <td>float16, int8, int4</td> 
   </tr>
   <tr>
        <td>Gemma-2-2b-it-GGUF</td> 
         <td>q4_k_m,q5_k_m</td> 
   </tr>
   <tr>
        <td>Qwen1.5-7B-Chat-GGUF</td> 
        <td>int8, int4, int2</td> 
   </tr>
   <tr>
        <td>Qwen2.5-7B-Instruct-GGUF</td> 
        <td>q4_k_m, q3_k_m, q2_k</td> 
   </tr>
   <tr>
        <td>Llama-3.2-3B-Instruct</td> 
        <td>q4_k_m</td> 
   </tr>
   <tr>
        <td>baichuan2-7b-chat-gguf</td> 
        <td>int8, int4, int2</td> 
   </tr>
   <tr>
        <td>Meta-Llama-3.1-8B-Instruct-GGUF</td> 
        <td>int2</td> 
   </tr>
</table>

## PDF影印版支持
本次更新在知识库或插件文件对话的上传文件时，支持`PDF影印版`上传，其中PDF影印版是指通过扫描纸质文档，将其转换为数字图像，以PDF格式保存的文件版本。
YuanChat使用文本识别引擎`Tesseract-OCR`对影印版PDF中纯图片提取文字进行分片处理，同时YuanChat使用`Poppler`库对PDF进行文档解析，优化OCR流程以解析特殊的PDF。

## 新增用户活跃统计
本次更新新增用户活跃度统计，包括`用户使用时段`、`用户活跃时间`、`模型下载次数`、`日活跃用户数`、`月活跃用户数`。采集信息不涉及隐私数据，此数据用于帮助我们了解应用的日常活跃程度，评估应用的长期吸引力和用户粘性，以便调整开发策略。

## 修复已知问题
1.修复模型切换后内存无法释放的问题；
2.修复应用关闭后后台无法退出的问题；
3.修复上传DOCX文档抛出异常的问题；
4.修复网络检索(bing检索)为空的问题；
5.修复模型初始化数据库内容缺失的问题；
6.修复自然语言处理包nltk_data缺失的问题。