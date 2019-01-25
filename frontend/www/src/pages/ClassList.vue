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
import { curriculumsService } from '../services';

export default {
  data() {
    return {
      list: [],
      listQuery: {
        filters: { curriculumName: undefined, curriculumCategory: undefined },
        sort: { curriculumNo: 'desc' },
        pagination: { pagenum: 1, limit: '' }
      },
    };
  },
  created () {
    curriculumsService.fetchCurriculmList(this.listQuery)
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