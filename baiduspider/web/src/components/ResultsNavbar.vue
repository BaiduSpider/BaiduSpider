<template>
  <v-app-bar
    color="primary"
    dark
  >

    <v-toolbar-title>
      <router-link to="/" class="title d-none d-lg-block d-sm-block d-md-block">BaiduSpider</router-link>
      <router-link to="/" class="title d-flex d-sm-none">
        <v-icon>
          mdi-home
        </v-icon>
      </router-link>
    </v-toolbar-title>
    <v-spacer/>
    <v-form
      @submit="search(queryData)"
      onSubmit="return false"
    >
      <v-text-field
        label="搜索"
        solo-inverted
        style="margin-top: 30px"
        flat
        autocomplete="off"
        v-model="queryData"
        class="search"
        append-icon="mdi-magnify"
        @click:append="search(queryData)"
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
.search {
  width: 80vw;
}
.title {
  cursor: hand;
  color: white !important;
  text-decoration: none;
}
</style>
