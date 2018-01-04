<template>
  <canvas :width="width" :height="height" ref="canvas"></canvas>
</template>

<script>
  import * as lsystem from '../lsystem.js'
  export default {
    props: {
      system: Object,
      width: {
        default: 450
      },
      height: {
        default: 450
      }
    },
    watch: {
      system: function () {
        this.render()
      }
    },
    mounted () {
      this.render()
    },
    methods: {
      render () {
        let canvas = this.$refs.canvas
        lsystem.render(canvas, this.system)
      }
    }
  }
</script>

<style scoped>
  canvas {
    background-color: #FFD;
    border: 1px solid;
    margin: 2px;
    border-color: #777;
  }
</style>
