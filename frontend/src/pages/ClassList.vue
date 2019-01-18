<template>
  <v-ons-page>
    <custom-toolbar v-bind="toolbarInfo"></custom-toolbar>

        <!-- Load more items on scroll bottom -->
        <v-ons-page>
          <ClassItem :list="list"></ClassItem>
        </v-ons-page>

  </v-ons-page>
</template>

<script>
import ClassItem from './ClassItem.vue';
import axios from 'axios'

const HTTP = axios.create({
    baseURL: `http://localhost:5000/api`,
    timeout: 5000,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  })

export default {
  data() {
    return {
      list: [],
      listQuery: {
        filters: { curriculumName: undefined, curriculumCategory: undefined },
        sort: { curriculumNo: 'desc' },
        pagination: { pagenum: 1, limit: 20 }
      },
    };
  },
  created () {
    HTTP.get(`resource/curriculums/filter`, {params: this.listQuery})
      .then(response => {
        this.list = response.data.return.items
      })
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