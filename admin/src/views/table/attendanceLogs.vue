<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.filters.curriculumNo" :placeholder="$t('table.attendanceLogs.curriculumCategory')" clearable class="filter-item" style="width: 250px">
        <el-option v-for="(item, index) in curriculumOptionlist" :key="index" :label="item.curriculumName+'('+item.ordinalNo+')'" :value="item.curriculumNo"/>
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">{{ $t('table.search') }}</el-button>
    </div>

    <el-table
      v-loading="listLoading"
      v-if="list.length > 0"
      :key="tableKey"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;">
      <el-table-column :label="$t('table.attendanceLogs.phoneNo')" prop="phoneNo" align="center" sortable>
        <template slot-scope="scope">
          <span>{{ scope.row.phoneNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.attendanceLogs.name')" align="center">
        <el-table-column v-for="(attendanceLog,index) of list.signatureTimestamp" :label="attendanceLog.attendanceDate" :key="index">
          <template slot-scope="scope">
            <span>{{ scope.row }}</span>
          </template>
        </el-table-column>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import { fetchAttendanceLogsList } from '@/api/resource/attendanceLogs'
import { fetchCurriculumList } from '@/api/resource/curriculums'
import waves from '@/directive/waves' // Waves directive

export default {
  name: 'AttendanceLogs',
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: [],
      curriculumOptionlist: null,
      total: 0,
      listLoading: false,
      listQuery: {
        filters: { curriculumNo: undefined }
      },
      curriculumOptionlistQuery: {
        filters: { curriculumNo: undefined },
        sort: { curriculumNo: 'desc' },
        pagination: { pagenum: 1, limit: '' }
      }
    }
  },
  created() {
    this.getCurriculumList()
  },
  methods: {
    getList() {
      this.listLoading = true
      const query = { curriculumNo: this.listQuery.filters.curriculumNo }
      fetchAttendanceLogsList(query).then(response => {
        const data = JSON.parse(response.data)
        console.log(data)
        this.list = data.return.items
        this.total = response.data.return.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    getCurriculumList() {
      fetchCurriculumList(this.curriculumOptionlistQuery).then(response => {
        this.curriculumOptionlist = response.data.return.items
      })
    },
    handleFilter() {
      if (!this.listQuery.filters.curriculumNo) {
        this.$notify({
          title: 'Failed',
          message: 'Select Curriculum option',
          type: 'warn',
          duration: 2000
        })
      } else {
        this.getList()
      }
    }
  }
}
</script>
