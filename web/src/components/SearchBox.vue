<template>
  <v-main>
    <v-container
      class="fill-height"
      fluid
    >
      <v-row
        align="center"
        justify="center"
        style="bottom: 200px; position: relative"
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
              @click:append-outer="searchWeb()"
            ></v-text-field>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  name: 'HelloWorld',

  data: () => {
    return {
      query: ''
    }
  },
  methods: {
    searchWeb: function () {
      console.log(this.query)
    }
  }
}
</script>
