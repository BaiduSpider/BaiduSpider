<template>
  <v-autocomplete
    v-model="select"
    :loading="loading"
    :items="items"
    :search-input.sync="search"
    class="search"
    flat
    clearable
    hide-details
    item-text="title"
    item-value="path"
    label="Search"
    append-icon="mdi-magnify"
    hide-no-data
    solo-inverted
  ></v-autocomplete>
</template>

<script>
import Flexsearch from "flexsearch"

export default {
  data () {
    return {
      index: null,
      loading: false,
      items: [],
      search: null,
      select: '123',
      results: [{}]
    }
  },
  watch: {
    search (val) {
      val && val.length > 1 && val !== this.select && this.querySelections(val)
    },
    select (val) {
      if (val) {
        this.$router.push(val)
      }
    }
  },
  mounted () {
    this.index = new Flexsearch({
      tokenize: "forward",
      doc: {
        id: "key",
        field: ["title"]
      }
    });
    const { pages } = this.$site;
    this.index.add(pages);
  },
  methods: {
    querySelections (v) {
      this.loading = true
      this.index.search(
        v,
        {
          limit: 10,
          threshold: 2,
          encode: 'extra'
        },
        (result) => {
          this.items = result
          this.loading = false
        })
    },
  },
}
</script>

<style lang="stylus" scoped>
.search
  margin-right: 20px
</style>