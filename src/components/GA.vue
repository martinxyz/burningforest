<template>
  <div>
    <div>
      <img src="../assets/template1.png">
      <b-button variant="primary" v-on:click="resample">Try Again!</b-button>
    </div>
    <div>
      <span v-for="s in sample">
        <l-display :system="s" width="67" height="126" />
      </span>
    </div>
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
        this.sample = ga.createGoodSamples()
      }
    }
  }
</script>

<style scoped>
  img {
    padding: 10px;
  }
</style>
