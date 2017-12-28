<template>
  <div id="app">
    <div id="topbar">
      <img src="./assets/logo.svg" style="height: 120px;">
    </div>
    <div id="main">
      <HelloL/>
    </div>
  </div>
</template>

<script>
import HelloL from './components/HelloL'

export default {
  name: 'app',
  components: {
    HelloL
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

body {
  margin: 0px;
}

#topbar {
  padding: 10px 10px 0px 10px;
  background-color: #eee;
  border-bottom: 2px solid;
  border-color: #aaa;
}

#main {
  /* margin: 0px 10px; */
}
</style>
