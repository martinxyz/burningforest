<template>
  <div class="layout-column" v-on:keydown="key" v-on:keyup="key">
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
    <div class="layout-row buttons">
      <b-button ref="a" v-on:click="prefer_a">prefer<br><b>A</b></b-button>
      <div class="layout-column buttons">
        <b-button ref="same" v-on:click="prefer_same">same<br><b>S</b></b-button>
        <b-button ref="skip" v-on:click="prefer_skip">skip<br><b>SPC</b></b-button>
      </div>
      <b-button ref="b" v-on:click="prefer_b">prefer<br><b>B</b></b-button>
    </div>
  </div>
</template>

<style scoped>
  .pair {
    justify-content: center;
    text-align: center;
  },
  /* .pair > div { */
  /* max-width: 10vw; */
  /* } */
  /* .pair.active > div { */
  /* max-width: 100vw; */
  /* } */
  .buttons {
    justify-content: center;
  }
  button {
    margin: 5px;
    min-width: 100px;
    transition: all 0.3s ease;
    /* background-color: #CCC; */
  }
  button.blink {
    transition: none 0s;
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
        debug: '...',
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
          this.debug = res.axiom
        })
        this.pairs[0].a = this.nextSample[0]
        this.pairs[0].b = this.nextSample[1]
        console.log('the new a:', this.pairs.a)
        setTimeout(() => {
          this.nextSample = ga.createGoodSamples(10)
        }, 0)
      },
      postit () {
        api.postit({foo: 'bar'})
      },
      key (ev) {
        /* console.log('ev', ev) */
        let keyMap = {
          prefer_a: ['a', 'ArrowLeft', 'h'],
          prefer_b: ['b', 'ArrowRight', 'l'],
          prefer_same: ['s', 'ArrowUp', 'k'],
          prefer_skip: [' ', 'ArrowDown', 'j']
        }
        _.forEach(keyMap, (keys, method) => {
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
        console.log('A better!')
        this.blink(this.$refs.a)
      },
      prefer_b () {
        console.log('B better!')
        this.blink(this.$refs.b)
      },
      prefer_same () {
        console.log('Same!')
        this.blink(this.$refs.same)
      },
      prefer_skip () {
        console.log('Skip!')
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
