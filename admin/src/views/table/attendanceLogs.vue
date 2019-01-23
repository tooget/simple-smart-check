<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.filters.curriculumNo" :placeholder="$t('table.attendanceLogs.curriculumCategory')" clearable class="filter-item" style="width: 400px">
        <el-option v-for="(item, index) in curriculumOptionlist" :key="index" :label="item.curriculumName+'('+item.ordinalNo+')'" :value="item.curriculumNo"/>
      </el-select>
      <el-button v-waves :loading="listLoading" class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">{{ $t('table.search') }}</el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleFileDownload">{{ $t('table.download') }}</el-button>
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
      <el-table-column :label="$t('table.attendanceLogs.phoneNo')" prop="phoneNo" width="135px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.phoneNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.attendanceLogs.applicantName')" prop="applicantName" width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.applicantName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.attendanceLogs.name')" align="center">
        <el-table-column v-for="(attendanceDate, index) of attendanceDates" :label="attendanceDate" :key="index" align="center">
          <el-table-column :label="$t('table.attendanceLogs.In')" width="100px" align="center">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.signatureTimestamp[index].In!==null" :type="scope.row.signatureTimestamp[index].In | statusFilter">{{ scope.row.signatureTimestamp[index].In | parseTime('{h}:{i}') }}</el-tag>
              <el-tag v-else :type="scope.row.signatureTimestamp[index].In | statusFilter">{{ $t('table.attendanceLogs.noSignature') }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column :label="$t('table.attendanceLogs.Out')" width="100px" align="center">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.signatureTimestamp[index].Out!==null" :type="scope.row.signatureTimestamp[index].Out | statusFilter">{{ scope.row.signatureTimestamp[index].Out | parseTime('{h}:{i}') }}</el-tag>
              <el-tag v-else :type="scope.row.signatureTimestamp[index].Out | statusFilter">{{ $t('table.attendanceLogs.noSignature') }}</el-tag>
            </template>
          </el-table-column>
        </el-table-column>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import { fetchAttendanceLogsList, fetchAttendanceLogsListfile } from '@/api/resource/attendanceLogs'
import { fetchCurriculumList } from '@/api/resource/curriculums'
import waves from '@/directive/waves' // Waves directive

export default {
  name: 'AttendanceLogs',
  directives: { waves },
  filters: {
    statusFilter(status) {
      if (status) {
        return 'success'
      } else {
        return 'danger'
      }
    }
  },
  data() {
    return {
      tableKey: 0,
      list: [],
      curriculumOptionlist: null,
      total: 0,
      downloadLoading: false,
      listLoading: false,
      listQuery: {
        filters: { curriculumNo: undefined }
      },
      curriculumOptionlistQuery: {
        filters: { curriculumNo: undefined },
        sort: { curriculumNo: 'desc' }
      }
    }
  },
  computed: {
    attendanceDates() {
      const attendanceDates = {}
      this.list.forEach(row => {
        row.signatureTimestamp.forEach(signature => {
          attendanceDates[signature.attendanceDate] = 1
        })
      })
      return Object.keys(attendanceDates)
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
        this.list = response.data.return.items
        this.total = response.data.return.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      }).catch(() => {
        this.$notify({
          title: 'Failed',
          message: 'Attendance Table is not exist',
          type: 'error',
          duration: 2000
        })
        this.listLoading = false
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
          message: 'Select Curriculum Option First',
          type: 'warning',
          duration: 2000
        })
      } else {
        this.getList()
      }
    },
    handleFileDownload() {
      if (!this.listQuery.filters.curriculumNo) {
        this.$notify({
          title: 'Failed',
          message: 'Select Curriculum Option First',
          type: 'warning',
          duration: 2000
        })
      } else {
        this.downloadAttendanceLogsListfile()
      }
    },
    downloadAttendanceLogsListfile() {
      const query = { curriculumNo: this.listQuery.filters.curriculumNo }
      fetchAttendanceLogsListfile(query).then(response => {
        this.downloadLoading = true
        const curriculumNoFromServer = response.config.params.curriculumNo
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'attendance_ID_' + curriculumNoFromServer + '.xlsx')
        document.body.appendChild(link)
        link.click()
        this.downloadLoading = false
        this.$notify({
          title: 'Succeeded',
          message: 'Attendance Table(excel file) downloaded',
          type: 'success',
          duration: 2000
        })
      }).catch(() => {
        this.$notify({
          title: 'Failed',
          message: 'Attendance Table(excel file) missing',
          type: 'error',
          duration: 2000
        })
      })
    }
  }
}
</script>
