<template>
  <SearchBox/>
</template>

<script>
import SearchBox from '@/components/SearchBox'

export default {
  name: 'Home',
  components: {
    SearchBox
  },
  created: function () {
    document.title = 'BaiduSpider'
  }
}
</script>
