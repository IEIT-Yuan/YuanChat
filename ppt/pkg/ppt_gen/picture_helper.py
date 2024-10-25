import requests
from io import BytesIO
from diffusers import DiffusionPipeline
from pkg.ppt_gen import config as config


#stable-diffusion-xl-base-1.0  12.105703115463257  可识别中文

def get_picture_from_url(query):
    if query == "":
        return None
    query = query.replace(",","+")
    url = config.url + query
    try:
        response = requests.get(url,timeout=(2,5))
    except requests.exceptions.ConnectionError:
        return None
    except:
        return None
    else:
        response.raise_for_status()
        pic_json = response.json()
        photos = pic_json["hits"]
        if len(photos) >= 1:
            photos_url = photos[0]["largeImageURL"]
            try:
                response = requests.get(photos_url,stream=True,verify=False,timeout=(2,5))
            except requests.exceptions.ConnectionError:
                return None
            except:
                return None
            else:
                image =BytesIO(response.content)

                return image
        else:
                return None
def get_picture_from_model_api_hug(query:str):
    def querys(payload):
        response = requests.post(config.API_URL, headers=config.HEADERS_API, json=payload)
        return response.content
    image_bytes = querys({
        "inputs": query,
    })
    image =BytesIO(image_bytes)
    return image
def get_picture_from_model_api_zhipu(query:str):
    from zhipuai import ZhipuAI 
    client = ZhipuAI(api_key=config.ZHIPU_API_KEY) 
    # 请填写您自己的APIKey 
    response = client.images.generations( model="cogview",prompt=query, ) 
    image = requests.get(response.data[0].url)
    return BytesIO(image.content)
def get_picture_from_model_huggingface(query:str):
    pipe = DiffusionPipeline.from_pretrained(config.MODEPATH)
    image = pipe(query).images[0]
    return BytesIO(image)



                                