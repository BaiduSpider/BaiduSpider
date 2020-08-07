<template>
  <v-app-bar color="primary" dark absolute>
    <SidebarButton @toggle-sidebar="$emit('toggle-sidebar')" />

    <v-toolbar-title
    >
      <router-link :to="$localePath" class="title">
        <img
          v-if="$site.themeConfig.logo"
          :src="$withBase($site.themeConfig.logo)"
          :alt="$siteTitle"
        >
        <span
          v-if="$siteTitle"
          ref="siteName"
          :class="{ 'can-hide': $site.themeConfig.logo }"
        >{{ $siteTitle }}</span>
      </router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <SearchBox v-if="$site.themeConfig.search !== false && $page.frontmatter.search !== false" />
    <NavLinks class="links" />
  </v-app-bar>
</template>

<script>
import SearchBox from './SearchBox'
import SidebarButton from './SidebarButton.vue'
import NavLinks from './NavLinks.vue'

export default {
  name: 'Navbar',

  components: {
    SidebarButton,
    NavLinks,
    SearchBox
  }
}
</script>

<style lang="stylus">
@media (max-width: $MQMobile)
  .links
    display none

.title
  color white !important
</style>
