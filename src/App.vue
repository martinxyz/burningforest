<template>
  <div id="app">
    <b-tabs class="tabsbg">
      <b-tab title="HelloL">
        <!-- <div id="topbar"> -->
        <!-- <img src="./assets/logo.svg" style="height: 120px;"> -->
        <!-- </div> -->
        <div id="main">
          <l-hello/>
        </div>
      </b-tab>
      <b-tab title="GA" active>
        <l-ga/>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import HelloL from './components/HelloL'
import GA from './components/GA'

export default {
  components: {
    'l-hello': HelloL,
    'l-ga': GA
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  padding-top: 2px;
}

body {
  margin: 0px;
  background-color: #eee;
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

div.tab-content {
  background-color: #fff;
  padding: 5px;
}

.nav-link {
  color: #000;
}
.nav-tabs {
  outline: none;
}

</style>
