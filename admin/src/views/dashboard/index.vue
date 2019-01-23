<template>
  <div class="dashboard-container">
    <div class="dashboard-text">{{ $t('table.dashboard.name') }}</div>
    <div class="filter-container">
      <el-select v-model="listQuery.filters.curriculumNo" :placeholder="$t('table.dashboard.curriculumCategory')" clearable class="filter-item" style="width: 250px">
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
      style="width: 100%;"
      @sort-change="sortChange">
      <el-table-column :label="$t('table.dashboard.curriculumNo')" prop="curriculumNo" sortable="custom" align="center" width="85px">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.dashboard.curriculumName')" prop="curriculumName" sortable="custom" width="230px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.dashboard.ordinalNo')" prop="ordinalNo" sortable="custom" width="85px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ordinalNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.dashboard.curriculumCategory')" prop="curriculumCategory" sortable="custom" width="120px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumCategory }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.dashboard.curriculumType')" prop="curriculumType" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumType }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.startDate')" prop="startDate" sortable="custom" width="95px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.startDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.endDate')" prop="endDate" sortable="custom" width="95px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.endDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.dashboard.ApplicantCount')" prop="ApplicantCount" sortable="custom" width="110px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ApplicantCount }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.dashboard.MemberCount')" prop="MemberCount" sortable="custom" width="110px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.MemberCount }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.dashboard.MemberCompleteCount')" prop="MemberCompleteCount" sortable="custom" width="110px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.MemberCompleteCount }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.dashboard.MemberEmploymentCount')" prop="MemberEmploymentCount" sortable="custom" width="110px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.MemberEmploymentCount }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.pagination.pagenum" :limit.sync="listQuery.pagination.limit" @pagination="getList" />

  </div>
</template>

<script>
import { fetchCurriculumWithMemberCountList, fetchCurriculumList } from '@/api/resource/curriculums'
import waves from '@/directive/waves' // Waves directive
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'Members',
  components: { Pagination },
  directives: { waves },
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
      fetchCurriculumWithMemberCountList(this.listQuery).then(response => {
        const message = response.data.message
        this.list = response.data.return.items
        this.total = response.data.return.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
        this.$notify({
          title: message.title,
          message: message.content,
          type: 'success',
          duration: 2000
        })
      }).catch(error => {
        const message = error.response.data.message
        this.$notify({
          title: message.title,
          message: message.content,
          type: 'error',
          duration: 2000
        })
      })
    },
    getCurriculumList() {
      fetchCurriculumList(this.curriculumOptionlistQuery).then(response => {
        this.curriculumOptionlist = response.data.return.items
      })
    },
    sortChange(data) {
      const { prop, order } = data
      const sortOption = { ascending: 'asc', descending: 'desc' }
      const sortChange = {}
      sortChange[prop] = sortOption[order]
      this.listQuery.sort = sortChange
      this.handleFilter()
    },
    handleFilter() {
      this.listQuery.pagination.pagenum = 1
      this.getList()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
