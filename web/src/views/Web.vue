<template>
  <div>
    <WebResults/>
  </div>
</template>

<script>
import WebResults from '@/components/WebResults.vue'

export default {
  name: 'Web',
  components: {
    WebResults
  },
  created: function () {
    document.title = `${this.$route.query.q} - BaiduSpider`
  },
  watch: {
    '$route.query.q': function () {
      document.title = `${this.$route.query.q} - BaiduSpider`
    }
  }
}
</script>
