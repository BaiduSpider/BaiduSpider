<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>

<script>
export default {
  name: 'App',

  created: function () {
    this.$vuetify.theme.dark = window.matchMedia('(prefers-color-scheme: dark)').matches
    window.matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', event => {
        this.$vuetify.theme.dark = event.matches
      })
  }
}
</script>
