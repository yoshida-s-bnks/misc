new Vue({
  el: '#app',
  data: {
    title: "hello world with Vue.js",
    subtitle: "also getting started with Bulma",
    value: "",
    counter: 1
  },
  methods: {
    increase: function(step, event) {
      this.counter += step;
    },
    halve: function(event) {
      if(this.counter > 1) {
        this.counter = Math.ceil(this.counter/2);
        this.value += this.value;
      }
    }
  }
})
