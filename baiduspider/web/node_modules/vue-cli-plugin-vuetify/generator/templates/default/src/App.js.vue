<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <%_ if (iconFont === 'mdi') { _%>
        <v-icon>mdi-open-in-new</v-icon>
        <%_ } else if (iconFont === 'md') { _%>
        <v-icon>open_in_new</v-icon>
        <%_ } else if (iconFont === 'fa') { _%>
        <v-icon>fas fa-external-link-alt</v-icon>
        <%_ } else if (iconFont === 'fa4') { _%>
        <v-icon>fa-external-link</v-icon>
        <%_ } _%>
      </v-btn>
    </v-app-bar>

    <v-content>
      <%_ if (router) { _%>
      <router-view/>
      <%_ } else { _%>
      <HelloWorld/>
      <%_ } _%>
    </v-content>
  </v-app>
</template>

<script>
<%_ if (!router) { _%>
import HelloWorld from './components/HelloWorld';
<%_ } _%>

export default {
  name: 'App',

  <%_ if (!router) { _%>
  components: {
    HelloWorld,
  },

  <%_ } _%>
  data: () => ({
    //
  }),
};
</script>
