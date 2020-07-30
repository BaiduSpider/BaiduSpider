<template>
  <div v-if="results[0]">
    <v-list two-line subheader>
      <v-list-item
        v-for="(news, index) in results"
        :key="index"
      >
        <v-list-item-content>
          <v-list-item-title>
            <a :href="news.url" target="_blank">
              {{ news.time }}
              &nbsp;-&nbsp;
              {{ news.title }}
            </a>
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ news.author }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-subheader>资讯</v-subheader>
    </v-list>
    <v-divider></v-divider>
  </div>
</template>

<script>
export default {
  name: 'WebNews',
  props: [
    'results'
  ]
}
</script>
