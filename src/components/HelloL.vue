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
    <l-display :system="system" />
  </div>
</template>

<script>
  import * as lsystem from '../lsystem.js'
  import _ from 'lodash'

  export default {
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
      calc3 () { return lsystem.expand(this.calc2, this.rules) },
      system () {
        return {
          axiom: this.axiom,
          rules: _.clone(this.rules),
          angle: this.angle,
          iterations: 3
        }
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
