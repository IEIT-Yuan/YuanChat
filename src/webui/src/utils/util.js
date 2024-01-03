export const HEX_MAP = 'ABCDEFGHIJKLMNUPQRSTUVWXYZabcdefghijklmnupqrstuvwxyz0123456789'

export function getRandom(max = Math.pow(2, 16)) {
  const arr = new Uint16Array(1)
  return Math.floor(window.crypto.getRandomValues(arr)[0] * (max / Math.pow(2, 16)))
}

export function UUID(length = 32) {
  return new Array(length)
    .fill(undefined)
    .map(() => HEX_MAP.charAt(getRandom(HEX_MAP.length)))
    .join('')
}

export function copy(text) {
  if (window.clipboardData) {
    window.clipboardData.setData('text', text)
  } else {
    ;(function (t) {
      document.oncopy = function (e) {
        e.clipboardData.setData('text', t)
        e.preventDefault()
        document.oncopy = null
      }
    })(text)
    document.execCommand('Copy')
  }
}

/**
 * 随机获取数组内的n个元素
 * @param arr
 * @param n
 * @returns {*}
 */
export function getRandomElements(arr, n) {
  // 先复制数组，以免修改原始数组
  const copyArr = arr.slice()

  // 如果n大于数组长度，将n设置为数组长度
  n = Math.min(n, copyArr.length)

  // 随机排序数组
  copyArr.sort(() => Math.random() - 0.5)

  // 截取数组的前n个元素
  return copyArr.slice(0, n)
}
