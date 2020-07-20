<template>
  <v-app-bar
    color="primary"
    dark
  >

    <v-toolbar-title
      class="d-none d-lg-block d-sm-block d-md-block"
    >
      <router-link to="/" class="title">BaiduSpider</router-link>
    </v-toolbar-title>
    <v-spacer/>
    <v-form
      @submit="search(queryData)"
      onSubmit="return false"
    >
      <v-text-field
        label="搜索"
        solo-inverted
        clearable
        hide-details
        flat
        clear-icon="mdi-close"
        autocomplete="off"
        v-model="queryData"
        class="search"
      ></v-text-field>
    </v-form>
  </v-app-bar>
</template>

<script>
export default {
  name: 'ResultsNavbar',
  props: [
    'search',
    'query'
  ],
  data: () => {
    return {
      queryData: ''
    }
  },
  created: function () {
    this.queryData = this.query
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
.title {
  cursor: hand;
  color: white !important;
  text-decoration: none;
}
</style>
