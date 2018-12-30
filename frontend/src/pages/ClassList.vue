<template>
  <v-ons-page>
    <custom-toolbar v-bind="toolbarInfo"></custom-toolbar>

        <!-- Load more items on scroll bottom -->
        <v-ons-page :infinite-scroll="loadMore">
          <p class="intro">
            Useful for loading more items when the scroll reaches the bottom of the page, typically after an asynchronous API call.<br><br>
          </p>

          <ClassItem
            :list="list"
          >
          </ClassItem>

          <div class="after-list">
            <v-ons-icon icon="fa-spinner" size="26px" spin></v-ons-icon>
          </div>
        </v-ons-page>

  </v-ons-page>
</template>

<script>
import ClassItem from './ClassItem.vue';

export default {
  data() {
    return {
      list: []
    };
  },
  beforeMount() {
    for (let i = 0; i < 30; i++) {
      this.list.push(i);
    }
  },
  methods: {
    loadMore(done) {
      setTimeout(() => {
        for (let i = 0; i < 10; i++) {
          this.list.push(this.list.length + i);
        }
        done();
      }, 600)
    }
  },
  components: { ClassItem }
};
</script>

<style scoped>
.after-list {
  margin: 20px;
  text-align: center;
}
</style>