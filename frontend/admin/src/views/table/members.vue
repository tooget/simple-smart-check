<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input :placeholder="$t('table.members.applicantName')" v-model="listQuery.filters.applicantName" style="width: 100px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-select v-model="listQuery.filters.curriculumNo" :placeholder="$t('table.members.curriculumCategory')" clearable class="filter-item" style="width: 400px">
        <el-option v-for="(item, index) in curriculumOptionlist" :key="index" :label="item.curriculumName+'('+item.ordinalNo+')'" :value="item.curriculumNo"/>
      </el-select>
      <el-button v-waves :loading="listLoading" class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">{{ $t('table.search') }}</el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">{{ $t('table.download') }}</el-button>
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
      <el-table-column :label="$t('table.members.phoneNo')" prop="phoneNo" sortable="custom" width="135px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.phoneNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.applicantName')" prop="applicantName" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.applicantName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.attendancePass.name')" prop="attendancePass" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <el-button v-if="scope.row.attendancePass=='Y'" :type="scope.row.attendancePass | statusFilter" size="mini" @click="handleModifyStatus(scope.row, 'attendancePass', 'N')">{{ $t('table.members.attendancePass.status.Y') }}</el-button>
          <el-button v-else-if="scope.row.attendancePass=='N'" :type="scope.row.attendancePass | statusFilter" size="mini" @click="handleModifyStatus(scope.row, 'attendancePass', null)">{{ $t('table.members.attendancePass.status.N') }}</el-button>
          <el-button v-else size="mini" @click="handleModifyStatus(scope.row, 'attendancePass', 'Y')">{{ $t('table.members.attendancePass.status.null') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.attendanceCheck.name')" prop="attendanceCheck" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <el-button v-if="scope.row.attendanceCheck=='Y'" :type="scope.row.attendanceCheck | statusFilter" size="mini" @click="handleModifyStatus(scope.row, 'attendanceCheck', 'N')">{{ $t('table.members.attendanceCheck.status.Y') }}</el-button>
          <el-button v-else-if="scope.row.attendanceCheck=='N'" :type="scope.row.attendanceCheck | statusFilter" size="mini" @click="handleModifyStatus(scope.row, 'attendanceCheck', null)">{{ $t('table.members.attendanceCheck.status.N') }}</el-button>
          <el-button v-else size="mini" @click="handleModifyStatus(scope.row, 'attendanceCheck', 'Y')">{{ $t('table.members.attendanceCheck.status.null') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.curriculumComplete.name')" prop="curriculumComplete" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <el-button v-if="scope.row.curriculumComplete=='Y'" :type="scope.row.curriculumComplete | statusFilter" size="mini" @click="handleModifyStatus(scope.row, 'curriculumComplete', 'N')">{{ $t('table.members.curriculumComplete.status.Y') }}</el-button>
          <el-button v-else-if="scope.row.curriculumComplete=='N'" :type="scope.row.curriculumComplete | statusFilter" size="mini" @click="handleModifyStatus(scope.row, 'curriculumComplete', null)">{{ $t('table.members.curriculumComplete.status.N') }}</el-button>
          <el-button v-else size="mini" @click="handleModifyStatus(scope.row, 'curriculumComplete', 'Y')">{{ $t('table.members.curriculumComplete.status.null') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.employment.name')" prop="employment" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <el-button v-if="scope.row.employment=='Y'" :type="scope.row.employment | statusFilter" size="mini" @click="handleModifyStatus(scope.row, 'employment', 'N')">{{ $t('table.members.employment.status.Y') }}</el-button>
          <el-button v-else-if="scope.row.employment=='N'" :type="scope.row.employment | statusFilter" size="mini" @click="handleModifyStatus(scope.row, 'employment', null)">{{ $t('table.members.employment.status.N') }}</el-button>
          <el-button v-else size="mini" @click="handleModifyStatus(scope.row, 'employment', 'Y')">{{ $t('table.members.employment.status.null') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.curriculumNo')" prop="curriculumNo" sortable="custom" align="center" width="85px">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.curriculumName')" prop="curriculumName" sortable="custom" width="200px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.ordinalNo')" prop="ordinalNo" sortable="custom" width="85px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ordinalNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.curriculumCategory')" prop="curriculumCategory" sortable="custom" width="120px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumCategory }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.startDate')" prop="startDate" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.startDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.endDate')" prop="endDate" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.endDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.birthDate')" prop="birthDate" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.birthDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.email')" prop="email" sortable="custom" width="160px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.email }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.affiliation')" prop="affiliation" sortable="custom" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.affiliation }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.department')" prop="department" sortable="custom" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.department }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.position')" prop="position" sortable="custom" width="90px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.position }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.job')" prop="job" sortable="custom" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.job }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.purposeSelection')" prop="purposeSelection" sortable="custom" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.purposeSelection }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.careerDuration')" prop="careerDuration" sortable="custom" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.careerDuration }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.agreeWithPersonalinfo')" prop="agreeWithPersonalinfo" sortable="custom" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.agreeWithPersonalinfo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.members.agreeWithMktMailSubscription')" prop="agreeWithMktMailSubscription" sortable="custom" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.agreeWithMktMailSubscription }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.pagination.pagenum" :limit.sync="listQuery.pagination.limit" @pagination="getList" />

  </div>
</template>

<script>
import { fetchMembersList, fetchMembersListfile, updateMembersData } from '@/api/resource/members'
import { fetchCurriculumsList } from '@/api/resource/curriculums'
import waves from '@/directive/waves' // Waves directive
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'Members',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        Y: 'success',
        N: 'danger'
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
      downloadLoading: false,
      listLoading: true,
      listQuery: {
        filters: { applicantName: undefined, curriculumNo: undefined },
        sort: { curriculumNo: 'desc' },
        pagination: { pagenum: 1, limit: 20 }
      },
      curriculumOptionlistQuery: {
        filters: { curriculumNo: undefined },
        sort: { curriculumNo: 'desc' }
      }
    }
  },
  created() {
    this.getList()
    this.getCurriculumsList()
  },
  methods: {
    getList() {
      this.listLoading = true
      if (this.listQuery.filters.curriculumNo === '') {
        this.listQuery.filters.curriculumNo = undefined
      }
      fetchMembersList(this.listQuery).then(response => {
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
    getCurriculumsList() {
      fetchCurriculumsList(this.curriculumOptionlistQuery).then(response => {
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
          type: 'error',
          duration: 2000
        })
      })
    },
    handleDownload() {
      const query = Object.assign({}, this.listQuery)
      delete query.pagination
      fetchMembersListfile(query).then(response => {
        this.downloadLoading = true
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'members.xlsx')
        document.body.appendChild(link)
        link.click()
        this.downloadLoading = false
        this.$notify({
          title: '성공',
          message: '수강생 명단 엑셀파일을 성공적으로 다운로드하였습니다.',
          type: 'success',
          duration: 2000
        })
      }).catch(() => {
        this.$notify({
          title: '실패',
          message: '수강생 명단 엑셀파일 다운로드에 실패하였습니다.',
          type: 'error',
          duration: 2000
        })
      })
    }
  }
}
</script>
