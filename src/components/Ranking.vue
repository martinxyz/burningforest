<template>
  <div class="layout-column" v-on:keydown="key" v-on:keyup="key">
    <h1>Select Preference</h1>
    <div class="layout-row center" v-for="p in pairs">
      <div>
        <h3>A</h3>
        <l-display :system="p.a" width="p.a.width" height="p.a.height" />
      </div>
      <div>
        <h3>B</h3>
        <l-display :system="p.b" width="p.b.width" height="p.b.height" />
      </div>
    </div>
    <div class="layout-row center">
      <b-button ref="a" v-on:click="prefer_a">prefer<br><b>A</b></b-button>
      <div class="layout-column center">
        <b-button ref="same" v-on:click="prefer_same">same<br><b>S</b></b-button>
        <b-button ref="skip" v-on:click="prefer_skip">skip<br><b>SPC</b></b-button>
      </div>
      <b-button ref="b" v-on:click="prefer_b">prefer<br><b>B</b></b-button>
    </div>
  </div>
</template>

<style scoped>
  .center {
    justify-content: center;
    text-align: center;
  }
  button {
    margin: 5px;
    min-width: 100px;
    transition: background-color 0.3s ease;
  }
  button.blink {
    transition: none;
    background-color: #000;
  }
</style>

<script>
  import _ from 'lodash'
  import * as api from '../api.js'
  import * as ga from '../ga.js'
  export default {
    data () {
      let dummy = {
        height: 30,
        width: 30,
        angle: '10',
        axiom: 'G',
        rules: {
          G: 'G++[F]',
          F: '-----F---[G]'
        }
      }
      return {
        pairs: [{
          a: dummy,
          b: dummy
        }],
        nextSample: [dummy, dummy]
      }
    },
    mounted () {
      this.$refs.skip.focus()
      this.resample()
    },
    methods: {
      resample () {
        api.sample().then((res) => {
          console.log('todo: process api sample response', res)
        })
        this.pairs[0].a = this.nextSample[0]
        this.pairs[0].b = this.nextSample[1]
        setTimeout(() => {
          this.nextSample = ga.createGoodSamples(10)
        }, 0)
      },
      postit () {
        api.postit({foo: 'bar'})
      },
      key (ev) {
        // console.log('ev', ev)
        let methodKeys = {
          prefer_a: ['a', 'ArrowLeft', 'h'],
          prefer_b: ['b', 'ArrowRight', 'l'],
          prefer_same: ['s', 'ArrowUp', 'k'],
          prefer_skip: [' ', 'ArrowDown', 'j']
        }
        _.forEach(methodKeys, (keys, method) => {
          if (keys.includes(ev.key)) {
            if (ev.type === 'keydown' && !ev.repeat) {
              this[method]()
            }
            ev.preventDefault()
            ev.stopPropagation()
          }
        })
      },
      prefer_a () {
        this.blink(this.$refs.a)
      },
      prefer_b () {
        this.blink(this.$refs.b)
      },
      prefer_same () {
        this.blink(this.$refs.same)
      },
      prefer_skip () {
        this.blink(this.$refs.skip)
      },
      blink (el) {
        el.classList.add('blink')
        setTimeout(() => el.classList.remove('blink'), 50)
        this.$refs.skip.focus()
        this.resample()
      }
    }
  }
</script>
