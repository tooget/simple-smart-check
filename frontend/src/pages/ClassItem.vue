<template>
    <v-ons-list>
        <v-ons-list-item v-for="(item, key) in list" :key="key"
            modifier="chevron"
            @click="transition(item)"
        >
            {{ item.curriculumName +' ('+ item.startDate +'~'+ item.endDate +')' }}
        </v-ons-list-item>
    </v-ons-list>
</template>

<script>
import ClassItemPage from './ClassItemPage.vue';

export default {
  data() {
    return {};
  },
  props: {
    list: Array
  },
  methods: {
    transition(name) {
      this.$store.commit('navigator/options', {
        // Sets animations
        item: name,
        // Resets default options
        callback: () => this.$store.commit('navigator/options', {})
      });
      this.$store.commit('navigator/push', {
        extends: ClassItemPage,
        data() {
          return {
            item: name,
            phoneNo: null,
            attendanceTypes: ['In', 'Out'],
            selectAttendanceType: null,
            vueSignaturePadOptions: {
              dotSize: (0.5 + 2.5) / 2,
              minWidth: 0.5,
              maxWidth: 2.5,
              throttle: 16,
              minDistance: 5,
              backgroundColor: 'rgba(0,255,255,0)',
              penColor: 'black',
              velocityFilterWeight: 0.7,
            }
          }
        }
      });
    }
  }
};
</script>