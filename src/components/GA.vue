<template>
  <div class="layout-row">
    <div>
      <img src="../assets/template1.png">
      <b-button variant="primary" v-on:click="resample">Try Again!</b-button>
    </div>
    <span v-for="s in sample">
      <l-display :system="s" size="80" />
    </span>
  </div>
</template>

<script>
  import * as ga from '../ga.js'
  export default {
    data () {
      return {
        sample: []
      }
    },
    mounted () {
      this.resample()
    },
    methods: {
      resample () {
        this.sample = []
        for (let i = 0; i < 84; i++) {
          this.sample.push(ga.createSample())
        }
      }
    }
  }
</script>

<style scoped>
  img {
    padding: 10px;
  }
</style>
