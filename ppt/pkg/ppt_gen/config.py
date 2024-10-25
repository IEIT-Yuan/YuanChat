# 配置文件


##配置图片生成的连接API和URL

# 选择图片生成方式: 1.pixabay 2.huggingface 3.zhipu 4.本地

MODE_SELECT = 3

# 1.使用pixabay网站API检索图片
# headers_url["API_KEY"]: pixabay检索使用的API密钥，可登录 pixabay官网注册账号后申请
headers_url = {
    "API_KEY": "xxxx-xxxx",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0",
}

# url:检索时使用的网络接口格式
URL = "https://pixabay.com/api/?key=" + headers_url["API_KEY"] + "&q="

# 2.使用huggingface的API检索图片
# API_URL: huggingface检索使用的模型接口，可登录huggingface官网找到想要的模型，从模型主页Deploy按钮中API接口中获得
API_URL = "https://api-inference.huggingface.co/models/adirik/flux-cinestill"

# headers_API: huggingface检索使用的API密钥，可登录 huggingface官网注册账号后申请 修改Bearer后的内容即可
HEADERS_API = {"Authorization": "Bearer hf_xxxx-xxxx"}

# 3.使用zhipu大模型的API生成图片
# ZHIPU_api_key:使用国内zhipu大模型的API密钥，可登录 zhipu官网注册账号后申请
ZHIPU_API_KEY = "xxxxxxxx.xxxxxxxx"

# 4.使用Huggingface上下载的本地的模型生成图片
# 通过Huggingface下载的模型，可使用Huggingface 上的 Diffusers库在本地使用模型生成图片；耗时长，电脑配置低不建议使用
MODEPATH = "google/ddpm-cat-256"

# Ollama服务
OLLAMA_SERVER_IP = "xx.xx.xx.xx"
OLLAMA_SERVER_PORT = "11434"
