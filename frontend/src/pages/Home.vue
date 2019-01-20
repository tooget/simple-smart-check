<template>
  <v-ons-page>
    <v-ons-card v-for="page of pages" :key="page.label"
      @click="push(page.component, page.label)"
    >
      <div class="title">{{ page.label }}</div>
      <div class="content">{{ page.desc }}</div>
    </v-ons-card>
  </v-ons-page>
</template>

<script>
import ClassList from './ClassList.vue';

export default {
  data () {
    return {
      pages: [
        {
          component: ClassList,
          label: '출석부',
          desc: '(해당 교육과정 클릭 후 입/퇴실 여부를 확인해 주세요)'
        }
      ]
    };
  },
  methods: {
    push(page, key) {
      this.$store.commit('navigator/push', {
        extends: page,
        data() {
          return {
            toolbarInfo: {
              backLabel: 'Home',
              title: key
            }
          }
        }
      });
    }
  }
};
</script>

<style>
ons-card {
  cursor: pointer;
  color: #333;
}
.card__title, .card--material__title {
  font-size: 20px;
}
</style>
