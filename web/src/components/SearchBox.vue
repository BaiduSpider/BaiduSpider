<template>
  <div>
    <v-container>
      <v-tabs
        v-model="tab"
        grow
        center-active
      >

        <v-tab
          v-for="item in items"
          :key="item"
        >
          {{ item }}
        </v-tab>
      </v-tabs>
      </v-container>
    <v-container
      class="fill-height"
      fluid
    >
      <v-row
        align="center"
        justify="center"
        style="margin-bottom: 300px"
      >
        <v-col
          cols="12"
          sm="8"
          class="text-center"
        >
          <h1>BaiduSpider</h1>
          <br>
          <v-divider/>
          <br>
          <v-form
            @submit="searchWeb()"
            onSubmit="return false"
          >
            <v-text-field
              v-model="query"
              label="搜索"
              solo-inverted
              rounded
              append-outer-icon="mdi-magnify"
              clearable
              clear-icon="mdi-close"
              autocomplete="off"
              @click:append-outer="searchWeb()"
            ></v-text-field>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'SearchBox',

  data: () => {
    return {
      query: '',
      tab: null,
      items: [
        '网页'
      ],
      offline: null
    }
  },
  methods: {
    searchWeb: function () {
      if (!this.query) {
        return
      }
      this.$router.push({
        path: '/search/web',
        query: {
          q: this.query
        }
      })
    }
  }
}
</script>
