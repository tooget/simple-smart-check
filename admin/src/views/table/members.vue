<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input :placeholder="$t('table.members.applicantName')" v-model="listQuery.filters.applicantName" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-select v-model="listQuery.filters.curriculumNo" :placeholder="$t('table.members.curriculumCategory')" clearable class="filter-item" style="width: 250px">
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
      <el-table-column :label="$t('table.members.phoneNo')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.phoneNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.curriculumNo')" prop="curriculumNo" sortable="custom" align="center" width="65">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.attendancePass.name')" width="110px" align="center">
        <template slot-scope="scope">
          <el-button v-if="scope.row.attendancePass=='Y'" size="mini" @click="handleModifyStatus(scope.row, 'attendancePass', 'N')">{{ $t('table.members.attendancePass.status.Y') }}</el-button>
          <el-button v-else-if="scope.row.attendancePass=='N'" size="mini" @click="handleModifyStatus(scope.row, 'attendancePass', '')">{{ $t('table.members.attendancePass.status.N') }}</el-button>
          <el-button v-else size="mini" @click="handleModifyStatus(scope.row, 'attendancePass', 'Y')">{{ $t('table.members.attendancePass.status.null') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.attendanceCheck.name')" width="110px" align="center">
        <template slot-scope="scope">
          <el-button v-if="scope.row.attendanceCheck=='Y'" size="mini" @click="handleModifyStatus(scope.row, 'attendanceCheck', 'N')">{{ $t('table.members.attendanceCheck.status.Y') }}</el-button>
          <el-button v-else-if="scope.row.attendanceCheck=='N'" size="mini" @click="handleModifyStatus(scope.row, 'attendanceCheck', '')">{{ $t('table.members.attendanceCheck.status.N') }}</el-button>
          <el-button v-else size="mini" @click="handleModifyStatus(scope.row, 'attendanceCheck', 'Y')">{{ $t('table.members.attendanceCheck.status.null') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.curriculumComplete.name')" width="110px" align="center">
        <template slot-scope="scope">
          <el-button v-if="scope.row.curriculumComplete=='Y'" size="mini" @click="handleModifyStatus(scope.row, 'curriculumComplete', 'N')">{{ $t('table.members.curriculumComplete.status.Y') }}</el-button>
          <el-button v-else-if="scope.row.curriculumComplete=='N'" size="mini" @click="handleModifyStatus(scope.row, 'curriculumComplete', '')">{{ $t('table.members.curriculumComplete.status.N') }}</el-button>
          <el-button v-else size="mini" @click="handleModifyStatus(scope.row, 'curriculumComplete', 'Y')">{{ $t('table.members.curriculumComplete.status.null') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.employment.name')" width="110px" align="center">
        <template slot-scope="scope">
          <el-button v-if="scope.row.employment=='Y'" size="mini" @click="handleModifyStatus(scope.row, 'employment', 'N')">{{ $t('table.members.employment.status.Y') }}</el-button>
          <el-button v-else-if="scope.row.employment=='N'" size="mini" @click="handleModifyStatus(scope.row, 'employment', '')">{{ $t('table.members.employment.status.N') }}</el-button>
          <el-button v-else size="mini" @click="handleModifyStatus(scope.row, 'employment', 'Y')">{{ $t('table.members.employment.status.null') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.ordinalNo')" width="110px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ordinalNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.curriculumName')" min-width="150px">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.curriculumCategory')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumCategory }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.startDate')" prop="startDate" sortable="custom" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.startDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.endDate')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.endDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.applicantName')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.applicantName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.birthDate')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.birthDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.email')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.email }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.affiliation')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.affiliation }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.department')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.department }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.position')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.position }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.job')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.job }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.purposeSelection')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.purposeSelection }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.careerDuration')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.careerDuration }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.agreeWithPersonalinfo')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.agreeWithPersonalinfo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.agreeWithMktMailSubscription')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.agreeWithMktMailSubscription }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.agreeWithMktMailSubscription')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.agreeWithMktMailSubscription }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.pagination.pagenum" :limit.sync="listQuery.pagination.limit" @pagination="getList" />

  </div>
</template>

<script>
import { fetchMembersList, updateMembersData } from '@/api/resource/members'
import { fetchCurriculumList } from '@/api/resource/curriculums'
import waves from '@/directive/waves' // Waves directive
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'Members',
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
        filters: { applicantName: undefined, curriculumNo: undefined },
        sort: { curriculumNo: 'desc' },
        pagination: { pagenum: 1, limit: 20 }
      },
      curriculumOptionlistQuery: {
        filters: { curriculumNo: undefined },
        sort: { curriculumNo: 'desc' },
        pagination: { pagenum: 1, limit: '' }
      },
      temp: {
        curriculumNo: undefined,
        phoneNo: undefined,
        attendancePass: '',
        attendanceCheck: '',
        curriculumComplete: '',
        employment: ''
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
    sortChange(data) {
      const sortOption = { ascending: 'asc', descending: 'desc' }
      const { prop, order } = data
      if (prop === 'curriculumNo') {
        this.listQuery.sort = { curriculumNo: sortOption[order] }
      }
      this.handleFilter()
    },
    handleFilter() {
      this.listQuery.pagination.pagenum = 1
      this.getList()
    },
    handleModifyStatus(row, column, status) {
      const updateRow = Object.assign({}, row)
      updateRow[column] = status
      updateMembersData(updateRow).then(response => {
        const argument = JSON.parse(response.data.return.argument)
        const message = response.data.message
        updateRow.attendancePass = argument.attendancePass
        updateRow.attendanceCheck = argument.attendanceCheck
        updateRow.curriculumComplete = argument.curriculumComplete
        updateRow.employment = argument.employment
        for (const v of this.list) {
          if (v.curriculumNo === argument.curriculumNo && v.phoneNo === argument.phoneNo) {
            const index = this.list.indexOf(v)
            this.list.splice(index, 1, updateRow)
            break
          }
        }
        this.dialogFormVisible = false
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
          type: 'warn',
          duration: 2000
        })
      })
    }
  }
}
</script>
