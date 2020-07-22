<template>
  <div>
    <ResultsNavbar :search="searchWeb" :query="query"/>
    <v-container>
      <small class="text--secondary">
        BaiduSpider共找到搜索结果约{{ results.results[0].result }}条
      </small>
      <p/>
      <WebCalc :results="resultsCalc"/>
      <WebResult :results="resultsNormal" :key="resultId"/>
      <v-pagination
        v-model="currentPage"
        :length="results.total"
        :total-visible="10"
      ></v-pagination>
    </v-container>
  </div>
</template>

<script>
import ResultsNavbar from '@/components/ResultsNavbar'
import SearchService from '@/services/SearchService'
import WebResult from '@/components/WebResult'
import WebCalc from '@/components/WebCalc'

export default {
  name: 'WebResults',
  data: () => {
    return {
      query: '',
      results: {
        results: [
          { result: 0 }
        ]
      },
      resultsNormal: [],
      resultId: 0,
      resultsCalc: {},
      currentPage: 1
    }
  },
  methods: {
    searchWeb: function (query) {
      if (!query) return
      // eslint-disable-next-line
      this.$router.push(`/search/web?q=${encodeURIComponent(query)}`).catch((err) => {
        // eslint-disable-next-line
        return
      })
    },
    getResults: async function () {
      await SearchService.searchWeb(this.query, this.page).then((data) => {
        this.resultsNormal = []
        this.resultsCalc = {}
        this.results = data.data.results
        var i
        for (i = 0; i < this.results.results.length; i++) {
          if (this.results.results[i].type === 'result') {
            this.resultsNormal.push(this.results.results[i])
          }
        }
        for (i = 0; i < this.results.results.length; i++) {
          if (this.results.results[i].type === 'calc') {
            this.resultsCalc = this.results.results[i]
          }
        }
        this.resultId += 1
      })
    }
  },
  components: {
    ResultsNavbar,
    WebResult,
    WebCalc
  },
  created: function () {
    this.query = this.$route.query.q
    this.page = this.$route.query.pn
    this.getResults()
  },
  watch: {
    '$route.query.q': function () {
      this.query = this.$route.query.q
      this.page = 1
      this.getResults()
    },
    currentPage: function () {
      this.page = this.currentPage
      this.getResults()
    }
  }
}
</script>

<style scoped>
@media screen and ( max-width: 400px ) {
  .search {
    width: 330px;
  }
}
@media screen and ( min-width: 1000px ) {
  .search {
    width: 950px;
  }
}
</style>
