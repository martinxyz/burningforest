<template>
  <div class="layout-column">
    <div>
      <b-button variant="primary" v-on:click="resample">Try Again!</b-button>
      <b-button variant="primary" v-on:click="postit">POST it!</b-button>
    </div>
    <!-- <h1>{{debug}}</h1> -->
    <h1>Select Preference</h1>
    <div class="layout-row pair" v-for="p in pairs">
      <div>
        <h3>A</h3>
        <l-display :system="p.a" width="p.a.width" height="p.a.height" />
      </div>
      <div>
        <h3>B</h3>
        <l-display :system="p.b" width="p.b.width" height="p.b.height" />
      </div>
    </div>
  </div>
</template>

<style scoped>
  .pair {
    justify-content: center;
    text-align: center;
  }
  /* .pair > div { */
  /* max-width: 10vw; */
  /* } */
  /* .pair.active > div { */
  /* max-width: 100vw; */
  /* } */
</style>

<script>
  import * as api from '../api.js'
  export default {
    data () {
      return {
        pairs: [{
          a: {
            height: 30,
            width: 30,
            angle: '10',
            axiom: 'GGGGGG',
            rules: {
              G: 'G++[F]',
              F: '-----F---[G]'
            }
          },
          b: {
            height: 30,
            width: 30,
            angle: '15',
            axiom: 'GG',
            rules: {
              G: '+G+[F]',
              F: '-F--[G]'
            }
          }
        }],
        debug: '...'
      }
    },
    mounted () {
      this.resample()
    },
    methods: {
      resample () {
        api.sample().then((res) => {
          this.debug = res.axiom
        })
        // this.sample = ga.createGoodSamples()
      },
      postit () {
        api.postit({foo: 'bar'})
      }
    }
  }
</script>
