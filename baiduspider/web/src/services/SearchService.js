import Api from '@/services/Api'

export default {
  /**
   * 搜索网页
   * @param {String} query 搜索关键词
   * @param {Number} page 搜索结果页码
   * @returns {Promise} 搜索结果
   */
  searchWeb: function (query, page = 1) {
    return Api().get(`/web?query=${encodeURIComponent(query)}&page=${page}`).then((data) => {
      return data
    })
  }
}
