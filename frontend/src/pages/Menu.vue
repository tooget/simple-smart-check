<template>
  <v-ons-page modifier="white">
    <div class="profile-pic">
      <img src="../assets/vue.png">
    </div>

    <v-ons-list-title>Links</v-ons-list-title>
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
    loadLink(url) {
      window.open(url, '_blank');
    }
  },
  data() {
    return {
      links: [
        {
          title: 'Google Docs',
          icon: 'ion-document-text',
          url: 'https://drive.google.com/drive/folders/1y1aqwNcGervvuFQIh9Z4AAKbhs0PwlPC'
        },
        {
          title: 'Bitbucket',
          icon: 'ion-social-github',
          url: 'https://bitbucket.org/yunsu246/simple-smart-check'
        },
        {
          title: 'Facebook',
          icon: 'ion-social-twitter',
          url: 'https://www.facebook.com/kisa118/'
        },
        {
          title: 'OnOffMix',
          icon: 'ion-chatboxes',
          url: 'https://www.onoffmix.com/'
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
