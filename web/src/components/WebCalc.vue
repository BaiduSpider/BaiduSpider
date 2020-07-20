<template>
  <div>
    <v-card elevation="0">
      <v-list-item three-line>
        <v-list-item-content>
          <div class="overline" v-text="results.process + '='"></div>
          <v-list-item-title class="headline mb-1" v-text="results.result"></v-list-item-title>
          <v-list-item-subtitle>计算</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'WebCalc',
  props: [
    'results'
  ]
}
</script>

<style>

</style>
