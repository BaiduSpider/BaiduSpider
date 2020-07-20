/**
 * Axios api 调用
 */
import axios from 'axios'
import config from '../config/config'

export default () => {
  return axios.create({
    // 后台主链接
    baseURL: config.serverURL
  })
}
