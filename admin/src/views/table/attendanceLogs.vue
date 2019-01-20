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
        <template slot-scope="scope">
          <el-table-column v-for="(item, index) in scope.row.signatureTimestamp" :key="index" :label="item.attendanceDate" prop="signatureTimestamp" align="center">
            {{ scope.row.signatureTimestamp[0].attending }}
          </el-table-column>
        </template>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import { fetchMembersList } from '@/api/resource/members'
import { fetchCurriculumList } from '@/api/resource/curriculums'
import waves from '@/directive/waves' // Waves directive
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'AttendanceLogs',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      curriculumOptionlist: null,
      total: 0,
      listLoading: true,
      listQuery: {
        filters: { curriculumNo: undefined },
        sort: { curriculumNo: 'desc' },
        pagination: { pagenum: 1, limit: 20 }
      },
      curriculumOptionlistQuery: {
        filters: { curriculumNo: undefined },
        sort: { curriculumNo: 'desc' },
        pagination: { pagenum: 1, limit: '' }
      }
    }
  },
  computed: {
    signatureTimestamps() {
      const signatureTimestamps = {}
      this.list.forEach(row => {
        console.log(row)
        row.signatureTimestamp.forEach(signatureTimestamp => {
          signatureTimestamps[signatureTimestamp.attendanceDate] = 1
        })
      })
      return Object.keys(signatureTimestamps)
    }
  },
  created() {
    this.getList()
    this.getCurriculumList()
  },
  methods: {
    getList() {
      this.listLoading = true
      if (this.listQuery.filters.curriculumNo === '') {
        this.listQuery.filters.curriculumNo = undefined
      }
      fetchMembersList(this.listQuery).then(response => {
        this.list = response.data.return.items
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
      this.listQuery.pagination.pagenum = 1
      this.getList()
    },
    cellFormatter(row, col) {
      const key = JSON.parse(col.property)
      const d = row.signatureTimestamp.find(r => r.name === key.room)
      if (d && d[key.property]) {
        return d[key.property]
      }
      return '0 '
    }
  }
}
</script>
