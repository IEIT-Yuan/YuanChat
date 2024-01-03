import { fetchEventSource } from '@microsoft/fetch-event-source'
// import { ACCESS_TOKEN } from '@/store/mutation-types';
// import { getToken } from '@/utils/token'

const BASE_URL = import.meta.env.MODE === 'development' ? '/api' : ''

const useSse = (
  url,
  {
    onmessage,
    onopen,
    openWhenHidden = true,
    params = {},
    onerror = (err) => {
      console.error(err)
      throw err
    }
  }
) => {
  return fetchEventSource(`${BASE_URL}${url}`, {
    method: 'post',
    onmessage,
    onopen,
    onerror,
    openWhenHidden, // 文档处于隐藏状态时，是否保持请求状态(非标准api, 需注意兼容性)
    body: JSON.stringify(params),
    headers: {
      // 'X-Auth-Token': getToken(),
      'Content-Type': 'application/json'
    }
  })
}

export default useSse
