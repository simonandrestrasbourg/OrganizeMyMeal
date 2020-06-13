var vm = new Vue({
  el: '#starting',
  delimiters: ['${','}'],
  data: {
    recipes: [],
    loading: false,
    currentRecipe: {},
    message: null,
    newRecipe: { 'name': null, 'duration': null, 'short_description': null, 'content': null},
  },
  mounted: function() {
    this.getRecipes();
  },
  methods: {
    getRecipes: function() {
    this.loading = true;
    this.$http.get('/api/recipe/')
        .then((response) => {
          this.recipes = response.data;
          this.loading = false;
        })
        .catch((err) => {
         this.loading = false;
         console.log(err);
        })
    },
    getRecipe: function(id) {
    this.loading = true;
    this.$http.get(`/api/recipe/${id}/`)
     .then((response) => {
       this.currentRecipe = response.data;
       this.loading = false;
     })
     .catch((err) => {
       this.loading = false;
       console.log(err);
     })
   },
   addRecipe: function() {
    this.loading = true;
    this.$http.post('/api/recipe/',this.newRecipe)
        .then((response) => {
          this.loading = false;
          this.getRecipes();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
   },
   updateRecipe: function() {
    this.loading = true;
    this.$http.put(`/api/recipe/${this.currentRecipe.recipe_id}/`,     this.currentRecipe)
        .then((response) => {
          this.loading = false;
          this.currentRecipe = response.data;
          this.getRecipes();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
   },
   deleteRecipe: function(id) {
    this.loading = true;
    this.$http.delete(`/api/recipe/${id}/` )
        .then((response) => {
          this.loading = false;
          this.getRecipes();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
  }}
 });
