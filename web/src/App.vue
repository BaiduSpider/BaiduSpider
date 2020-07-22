<template>
  <v-app>
    <router-view></router-view>
    <v-overlay absolute :value="loading||offline" opacity="0.8">
      <v-progress-circular indeterminate size="64" v-if="!offline"></v-progress-circular>
      <div class="text-center" v-else>
        <h1>无法连接到API</h1>
        <p>请开启API后，刷新此页。</p>
      </div>
    </v-overlay>
  </v-app>
</template>

<script>
import StatusService from '@/services/StatusService'

export default {
  name: 'App',
  data: () => {
    return {
      offline: false,
      loading: true
    }
  },
  methods: {
    getStatus: async function () {
      let online
      await StatusService.getStatus().then((data) => {
        online = true
      }).catch(() => {
        online = false
      })
      this.offline = !online
      this.loading = false
    }
  },
  created: function () {
    this.getStatus()
    this.$vuetify.theme.dark = window.matchMedia('(prefers-color-scheme: dark)').matches
    if (window.matchMedia('(prefers-color-scheme: dark)').addEventListener) {
      window.matchMedia('(prefers-color-scheme: dark)')
        .addEventListener('change', event => {
          this.$vuetify.theme.dark = event.matches
        })
    }
  }
}
</script>
