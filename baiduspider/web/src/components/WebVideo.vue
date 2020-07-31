<template>
  <div v-if="results[0]">
    <v-list>
      <v-list-item>
        <v-row>
          <v-col
            cols="12"
            v-for="(video, index) in results"
            :key="index"
            lg="3"
            sm="4"
            xl="6"
          >
            <v-card max-width="320" outlined>
              <v-hover v-slot:default="{ hover }">
                <div>
                  <v-img :src="video.cover">
                    <v-chip
                      color="grey darken-3"
                      text-color="white"
                      style="float: right; margin-right: 5px; margin-top: 10px"
                      small
                    >
                      {{ video.length }}
                    </v-chip>
                    <v-fade-transition>
                      <v-overlay
                        v-if="hover"
                        absolute
                      >
                        <v-btn
                          :class="{ 'show-btns': hover }"
                          icon
                          :href="video.url"
                          target="_blank"
                        >
                          <v-icon :class="{ 'show-btns': hover }">
                            mdi-play
                          </v-icon>
                        </v-btn>
                      </v-overlay>
                    </v-fade-transition>
                  </v-img>
                </div>
              </v-hover>

              <v-card-text>
                <h3 style="margin-bottom: 5px">
                  <a :href="video.url" target="_blank">
                    {{ video.title }}
                  </a>
                </h3>
                {{ video.origin }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-list-item>
      <v-subheader>
        视频
      </v-subheader>
    </v-list>
    <v-divider></v-divider>
  </div>
</template>

<script>
export default {
  name: 'WebVideo',
  props: [
    'results'
  ]
}
</script>

<style>
.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}
a {
  text-decoration: none;
}
</style>
