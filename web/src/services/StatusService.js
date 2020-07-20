import Api from '@/services/Api'

export default {
  /**
   * 获取当前状态
   */
  getStatus: function () {
    return Api().get('/status').then((data) => {
      return data
    })
  }
}
