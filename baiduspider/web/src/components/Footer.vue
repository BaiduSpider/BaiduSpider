<template>
  <div style="margin-top: 100px">
    <v-footer
      absolute
      class="font-weight-medium"
    >
      <v-col
        class="text-center"
        cols="12"
      >
        <!--
        <v-divider style="margin-bottom: 15px"></v-divider>
        -->
        &copy;&nbsp;
        {{ new Date().getFullYear() }}
        &nbsp;—&nbsp;
        <strong>BaiduSpider</strong>
        <br/>
        <div style="margin-top: 5px"/>
        <strong>
          <a href="https://github.com/samzhangjy/BaiduSpider" target="_blank">
            GitHub
          </a>
        </strong>
        &nbsp;|&nbsp;
        <strong>
          <a href="https://samzhangjy.github.io/BaiduSpider" target="_blank">
            文档
          </a>
        </strong>
      </v-col>
    </v-footer>
  </div>
</template>

<script>
export default {
  name: 'Footer'
}
</script>
