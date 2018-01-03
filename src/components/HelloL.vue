<template>
  <div class="layout-row">
    <div class="tile layout-column inputs">
      <label>Angle <input v-model="angle"></label>
      <label>Start <input v-model="axiom"></label>
      <label v-for="s in usedSymbols">{{s}} <input v-model="rules[s]"></label>
      <div class="layout-column expansions">
        <span class="mono">{{axiom}}</span>
        <span class="mono">{{calc1}}</span>
        <span class="mono">{{calc2}}</span>
        <span class="mono">{{calc3}}</span>
      </div>
    </div>
    <div>
      <canvas width="440" height="440" ref="canvas"></canvas>
    </div>
  </div>
</template>

<script>
  import * as lsystem from '../lsystem.js'
  export default {
    /* name: 'HelloWorld', */
    data () {
      return {
        angle: '10',
        axiom: 'GGGGGG',
        rules: {
          G: 'G++[F]',
          F: '-----F---[G]'
        }
      }
    },
    computed: {
      usedSymbols () {
        let s = new Set()
        let addSymbolsOfRule = (rule) => {
          for (let c of rule) {
            if (lsystem.terminalSymbols.has(c)) continue
            if (!s.has(c)) {
              s.add(c)
              let rule = this.rules[c]
              if (rule) addSymbolsOfRule(rule)
            }
          }
        }
        addSymbolsOfRule(this.axiom)
        return [...s.keys()]
      },
      calc1 () { return lsystem.expand(this.axiom, this.rules) },
      calc2 () { return lsystem.expand(this.calc1, this.rules) },
      calc3 () { return lsystem.expand(this.calc2, this.rules) }
    },
    watch: {
      calc3 (value) {
        this.render()
      },
      angle (value) {
        this.render()
      }
    },
    mounted () {
      this.render()
    },
    methods: {
      render () {
        let canvas = this.$refs.canvas
        console.log('rendering:', this.calc3)
        lsystem.render(canvas, this.calc3, this.angle)
      }
    }
  }
</script>

<style scoped>
  .layout-row {
    display: flex;
    flex-direction: row;
  }
  .layout-column {
    display: flex;
    flex-direction: column;
  }
  .tile {
    width: 800px;
    flex-grow: 1;
    margin: 8px;
    /* border-color: #eee; */
    /* border: 1px; */
  }
  canvas {
    /* min-width: 300px; */
    /* min-height: 300px; */
    background-color: #EED;
    border: 4px solid;
    border-color: #ddd;
  }
  .inputs label {
    margin-bottom: 5px;
    text-align: right;
  }
  .expansions {
    /* justify-content: center; */
    text-align: center;
    border: 4px solid;
    border-color: #ddd;
    background-color: #EED;
  }
  .expansions span {
    padding-top: 8px;
    border-top: solid 1px;
    border-color: #ddd;
  }
  .expansions span:first-child {
    padding-top: 0px;
    border-top: none;
  }
  .mono {
    font-family: monospace;
    font-size: 17px;
  }
</style>
