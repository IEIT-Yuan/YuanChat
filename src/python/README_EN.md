<div align="center">

# Yuanchat Server Introduce

English / [简体中文](./README.md)

</div>


## Yuan2.0 Inference Server Deploy

[Yuan-2.0](https://github.com/IEIT-Yuan/Yuan-2.0/tree/main), deploy docker [instruction](https://github.com/IEIT-Yuan/Yuan-2.0/blob/main/README-EN.md#quick-start), run inference get model request url http://127.0.0.1:8000 [instruction](https://github.com/IEIT-Yuan/Yuan-2.0/blob/main/docs/inference_server.md)

## API Server Deploy
You can run the `docker_build.sh` to build the image, and then run the `docker_run.sh` to run a docker container, which located on the root path.
Attention, if your Yuan2.0 model server deployed at another machine, you need to add a `-e YUAN_2_URL=http://ip:port/yuan` in your docker run command
to specify the Yuan2.0 model address.

## API Server Introduce

We provide only one interface for UI in our back end service. The code is written in Python language. provided in a
Restful manner, and interacts with the UI in SSE(Server Send Event) mode.

Interface info follows: 

**interface url**: 

`http://ip:port/sse/subscribe`

here, ip is you server ip which deploy the docker image, and the port is exposed by 5050 in docker(referred the `docker_run.sh`).
this means you can use `http://ip:5050/sse/subscribe` to get the result.

**Http Method**: `POST`

**Content-Type**: `application/json`

**Response Content-Type**: `text/event-stream`

**Description**: user send the request, and get the result of Yuan2.0

**Request Params**: 

| param           | param description                                                                                                                                                                                                                                        | param type        | necessary | note                                                             |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------- | :-------- |:-----------------------------------------------------------------|
| messages        | user request                                                                                                                                                                                                                                             | list[dict_object] | yes       | detail info referred bellow                                      |
| response_length | the max token length of Yuan2.0 results. The larger the parameter setting, the longer it takes for the model to generate answers. Setting it too short may affect the integrity of the generated results. Token may be a word, word, or punctuation mark | int               | no        | default value:5000, range[0,8000]                                |
| temperature     | The larger the temperature value, the stronger the creativity of the model, but the generation effect is unstable.The smaller the temperature value, the stronger the stability of the model and the more stable the generation effect.                  | float             | no        | default value:0.6, range:[0,1]                                   |
| top_p           | The probability accumulation of generating tokens starts from the token with the highest probability and stops when the accumulation value is greater than or equal to top_p. When top_p is 0, this parameter has no effect.                             | float             | no        | default value:0.95, range:[0,1], can not be effective with top_k |
| top_k           | Select the k tokens with the highest probability as the candidate set. If the value of k is 1, then the answer is unique. When top*k is 0, this parameter has no effect. This parameter is related to top* p cannot work simultaneously.                 | int               | no        | default value:0, range:[0,10], can not be effective with top_p   |

detail introduction for dict_object in message:
message is a dict type param, and use to transfer multi dialog info, the length is recommended to be less than 10.

| param    | param description | param type | necessary | note                                                                                                                                              |
| :------- | :---------------- | :--------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| question | user request      | string     | yes       | The value is the user's historical request information                                                                                            |
| answer   | Yuan2.0 result    | string     | no        | The value is the system's historical inference result, corresponding one-to-one with the question, and the last one can be set as an empty string |

**Example**: 

```
{
	"messages":[
            {
                "question": "你好",
                "answer": "你好"
            },
            {
                "question": "1+1=?",
                "answer": ""
            }
        ],
	"top_p":0.95,
	"top_k":0,
	"response_length":50,
	"temperature":0.6
}
```

**Response Info**: 

| param        | param description       | param type  | necessary                                                 | note |
| :----------- | :---------------------- | :---------- |:----------------------------------------------------------| :--- |
| errCode      | error code of result    | string      | error code of Yuan2.0 result                              |
| errMessage   | error message of result | string      | error message of Yuan2.0 result                           |
| exceptionMsg | exception info          | string      | exception info                                            |
| flag         | status of result        | boolean     | status of result, true:system normal, false: system error |
| resData      | result info             | dict_object | result info of Yuan2.0, detail refers next                |

detail info for dict_object of resData:

| param   | param description | param type | necessary                     | note |
| :------ | :---------------- | :--------- | :---------------------------- | :--- |
| message | detail of result  | string     |                               |
| time    | time of result    | int        | time info, 13 digit timestamp |

The above is the description of the backend interface service.
If secondary development is required, you can go to the code `/src/python/yuan_process` to view and modify in `yuanchat.py`.

