<template>
  <div class="layout-row">
    <div class="tile layout-column inputs">
      <label>Start <input v-model="axiom"></label>
      <label>Rule G <input v-model="rule1"></label>
      <div class="layout-column expansions">
        <span class="mono">{{axiom}}</span>
        <span class="mono">{{calc1}}</span>
        <span class="mono">{{calc2}}</span>
        <span class="mono">{{calc3}}</span>
      </div>
    </div>
    <canvas class="tile"></canvas>
  </div>
</template>

<script>
  import * as lsystem from '../lsystem.js'
  export default {
    name: 'HelloWorld',
    data () {
      return {
        axiom: 'G',
        rule1: '-G-'
      }
    },
    computed: {
      rules () {
        return {'G': this.rule1}
      },
      calc1 () { return lsystem.expand(this.axiom, this.rules) },
      calc2 () { return lsystem.expand(this.calc1, this.rules) },
      calc3 () { return lsystem.expand(this.calc2, this.rules) }
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
    min-width: 300px;
    min-height: 300px;
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
    /* font-family: monospace; */
  }
</style>
