<template>
  <div>
    <v-list>
      <v-list-item
        v-for="(result, index) in results"
        :key="index"
      >
        <v-list-item-content>
          <a :href="result.url" target="_blank" style="margin-bottom: 10px">
            <v-list-item-title v-text="result.title"></v-list-item-title>
          </a>
          <v-list-item-subtitle>
            <span>
              {{ result.time }}&nbsp;-&nbsp;
            </span>
            {{ getDes(result.des) }}
            <p class="text--primary" style="margin-top: 10px">
              {{ result.origin }}
            </p>
          </v-list-item-subtitle>
          <v-divider></v-divider>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </div>
</template>

<script>
export default {
  name: 'WebResult',
  props: [
    'results'
  ],
  methods: {
    getDes: function (originalDes) {
      try {
        if (originalDes.split('-')[0].length <= 11) {
          return originalDes.split('-')[1]
        }
        return originalDes.split('-')[0]
      } catch (err) {
        return ''
      }
    }
  }
}
</script>
