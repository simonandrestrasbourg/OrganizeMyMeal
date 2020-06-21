Vue.component('card-recipe', {
  data: {
    recipes: [],
    loading: false,
    currentRecipe: {},
    message: null,
    newRecipe: { 'name': null, 'duration': null, 'short_description': null, 'content': null},
  },
  template: '#card-recipe',
})
