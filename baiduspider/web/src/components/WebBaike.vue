<template>
  <div v-if="result.title">
    <v-card
      outlined
    >
      <video v-if="result['cover-type'] === 'video'" :src="result.cover"></video>
      <div class="d-flex flex-no-wrap justify-space-between">
        <v-avatar
          class="ma-3"
          size="125"
          tile
          v-if="result['cover-type'] === 'image'"
        >
          <v-img :src="result.cover"></v-img>
        </v-avatar>
        <div>
          <v-card-title class="headline mb-1">
            <a :href="result.url" target="_blank">
              {{ result.title }}
            </a>
          </v-card-title>
          <v-card-subtitle>
            {{ result.des }}
          </v-card-subtitle>
        </div>
      </div>
      <v-card-text>
        <div class="overline mb-4">百科</div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'WebBaike',
  props: [
    'result'
  ]
}
</script>
