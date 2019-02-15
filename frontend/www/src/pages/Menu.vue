<template>
  <v-ons-page modifier="white">
    <v-ons-list-title>세션관리</v-ons-list-title>
    <v-ons-list>
      <v-ons-list-item v-for="item in logOut" :key="item.title"
        :modifier="md ? 'nodivider' : ''"
        @click="logout"
      >
        <div class="left">
          <v-ons-icon fixed-width class="list-item__icon" :icon="item.icon"></v-ons-icon>
        </div>
        <div class="center">
          {{ item.title }}
        </div>
        <div class="right">
          <v-ons-icon icon="fa-external-link"></v-ons-icon>
        </div>
      </v-ons-list-item>
    </v-ons-list>

    <v-ons-list-title>외부링크</v-ons-list-title>
    <v-ons-list>
      <v-ons-list-item v-for="item in links" :key="item.title"
        :modifier="md ? 'nodivider' : ''"
        @click="loadLink(item.url)"
      >
        <div class="left">
          <v-ons-icon fixed-width class="list-item__icon" :icon="item.icon"></v-ons-icon>
        </div>
        <div class="center">
          {{ item.title }}
        </div>
        <div class="right">
          <v-ons-icon icon="fa-external-link"></v-ons-icon>
        </div>
      </v-ons-list-item>
    </v-ons-list>
  </v-ons-page>
</template>

<script>
export default {
  methods: {
    loadView(index) {
      this.$store.commit('tabbar/set', index + 1);
      this.$store.commit('splitter/toggle');
    },
    logout(url) {
      const { dispatch } = this.$store;
      this.$store.commit('splitter/toggle');
      dispatch('logout');
    },
    loadLink(url) {
      window.open(url, '_blank');
    }
  },
  data() {
    return {
      logOut: [
        {
          title: '로그아웃',
          icon: 'ion-log-out',
          url: '/login'
        }
      ],
      links: [
        {
          title: '관리자 페이지',
          icon: 'ion-stats-bars',
          url: 'https://admin.smartcheck.gq'
        }
      ]
    };
  }
};
</script>

<style scoped>
.profile-pic {
  width: 100%;
  background-color: #fff;
  border-bottom: 1px solid #DDD;
  color: rgba(0, 0, 0, .56);
  padding-bottom: 8px;
  vertical-align: middle;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.page--material .profile-pic {
  background-color: #f6f6f6;
}

.profile-pic > img {
  display: block;
  max-width: 100%;
}
</style>

<style>
.page--material__background.page--white__background {
  background-color: #fff;
}
</style>
