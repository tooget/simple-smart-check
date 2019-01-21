<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input :placeholder="$t('table.curriculums.curriculumName')" v-model="listQuery.filters.curriculumName" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-select v-model="listQuery.filters.curriculumCategory" :placeholder="$t('table.curriculums.curriculumCategory')" clearable class="filter-item" style="width: 130px">
        <el-option v-for="(item, index) in curriculumCategoryOptions" :key="index" :label="item.display_name" :value="item.key"/>
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">{{ $t('table.search') }}</el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">{{ $t('table.add') }}</el-button>
      <el-checkbox v-model="showApplicantsBulkInserted" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">{{ $t($t('table.curriculums.applicantsBulkInserted')) }}</el-checkbox>
      <el-checkbox v-model="showDonwnloadAtendanceLogs" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">{{ $t($t('table.curriculums.donwnloadAtendanceLogs')) }}</el-checkbox>
      <el-checkbox v-model="showDelete" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">{{ $t($t('table.curriculums.delete')) }}</el-checkbox>
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
      <el-table-column :label="$t('table.curriculums.curriculumNo')" prop="curriculumNo" sortable="custom" align="center" width="65">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.curriculumCategory')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumCategory }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.ordinalNo')" width="110px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ordinalNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.curriculumName')" width="150px" align="center">
        <template slot-scope="scope">
          <span class="link-type" @click="handleUpdate(scope.row)">{{ scope.row.curriculumName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.curriculumType')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.curriculumType }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.startDate')" prop="startDate" sortable="custom" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.startDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.endDate')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.endDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showApplicantsBulkInserted" :label="$t('table.curriculums.applicantsBulkInserted')" align="center" width="150" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <input ref="excel-upload-input" class="excel-upload-input" type="file" accept=".xlsx, .xls" @change="handleFileUpload">
          <el-button :loading="uploadExcelLoading" size="mini" type="primary" @click="handleFileSubmit(scope.row)">{{ $t('table.browse') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="showDonwnloadAtendanceLogs" :label="$t('table.curriculums.donwnloadAtendanceLogs')" align="center" width="150" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button v-waves :loading="downloadLoading" size="mini" type="primary" @click="handleFileDownload(scope.row)">{{ $t('table.download') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="showDelete" :label="$t('table.curriculums.delete')" align="center" width="100" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">{{ $t('table.delete') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.insertedTimestamp')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.insertedTimestamp | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.updatedTimestamp')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.updatedTimestamp | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.pagination.pagenum" :limit.sync="listQuery.pagination.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="150px" style="width: 450px; margin-left:50px;">
        <el-form-item :label="$t('table.curriculums.curriculumCategory')" prop="curriculumCategory">
          <el-input v-model="temp.curriculumCategory" :placeholder="$t('table.curriculums.curriculumCategory')"/>
        </el-form-item>
        <el-form-item :label="$t('table.curriculums.ordinalNo')" prop="ordinalNo">
          <el-input v-model="temp.ordinalNo" :placeholder="$t('table.curriculums.ordinalNo')"/>
        </el-form-item>
        <el-form-item :label="$t('table.curriculums.curriculumName')" prop="curriculumName">
          <el-input v-model="temp.curriculumName" :placeholder="$t('table.curriculums.curriculumName')"/>
        </el-form-item>
        <el-form-item :label="$t('table.curriculums.curriculumType')" prop="curriculumType">
          <el-input v-model="temp.curriculumType" :placeholder="$t('table.curriculums.curriculumType')"/>
        </el-form-item>
        <el-form-item :label="$t('table.curriculums.startDate')" prop="startDate">
          <el-date-picker v-model="temp.startDate" type="date" placeholder="Please pick a date"/>
        </el-form-item>
        <el-form-item :label="$t('table.curriculums.endDate')" prop="endDate">
          <el-date-picker v-model="temp.endDate" type="date" placeholder="Please pick a date"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('table.cancel') }}</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">{{ $t('table.confirm') }}</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { fetchCurriculumList, createCurriculumData, updateCurriculumData, deleteCurriculumData } from '@/api/resource/curriculums'
import { createApplicantsBulk } from '@/api/resource/applicants'
import { fetchAttendanceLogsListfile } from '@/api/resource/attendanceLogs'
import waves from '@/directive/waves' // Waves directive
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

const curriculumCategoryOptions = [
  { key: '단기과정', display_name: '단기과정' },
  { key: '집중과정', display_name: '집중과정' },
  { key: '고급과정', display_name: '고급과정' }
]

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      downloadLoading: false,
      listLoading: true,
      listQuery: {
        filters: { curriculumName: undefined, curriculumCategory: undefined },
        sort: { curriculumNo: 'desc' },
        pagination: { pagenum: 1, limit: 20 }
      },
      curriculumCategoryOptions,
      showApplicantsBulkInserted: false,
      showDonwnloadAtendanceLogs: false,
      showDelete: false,
      temp: {
        curriculumNo: undefined,
        curriculumCategory: '',
        ordinalNo: '',
        curriculumName: '',
        curriculumType: '',
        startDate: new Date(),
        endDate: new Date()
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      rules: {
        curriculumCategory: [{ required: true, message: 'curriculumCategory is required', trigger: 'blur' }],
        ordinalNo: [{ required: true, message: 'ordinalNo is required', trigger: 'blur' }],
        curriculumName: [{ required: true, message: 'curriculumName is required', trigger: 'blur' }],
        curriculumType: [{ required: true, message: 'curriculumType is required', trigger: 'blur' }],
        startDate: [{ type: 'date', required: true, message: 'startDate is required', trigger: 'change' }],
        endDate: [{ type: 'date', required: true, message: 'endDate is required', trigger: 'change' }]
      },
      uploadExcelLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchCurriculumList(this.listQuery).then(response => {
        this.list = response.data.return.items
        this.total = response.data.return.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.pagination.pagenum = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const sortOption = { ascending: 'asc', descending: 'desc' }
      const { prop, order } = data
      if (prop === 'curriculumNo') {
        this.listQuery.sort = { curriculumNo: sortOption[order] }
      }
      if (prop === 'startDate') {
        this.listQuery.sort = { startDate: sortOption[order] }
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        curriculumNo: undefined,
        curriculumCategory: '',
        ordinalNo: '',
        curriculumName: '',
        curriculumType: '',
        startDate: new Date(),
        endDate: new Date(),
        applicantsBulkXlsxFile: undefined
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp) // copy obj
          tempData.startDate = +new Date(tempData.startDate) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          tempData.endDate = +new Date(tempData.endDate) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          createCurriculumData(tempData).then(response => {
            const argument = JSON.parse(response.data.return.argument)
            const message = response.data.message
            this.list.unshift(argument)
            this.dialogFormVisible = false
            this.$notify({
              title: message.title,
              message: message.content,
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.curriculumNo = row.curriculumNo
      this.temp.startDate = new Date(this.temp.startDate)
      this.temp.endDate = new Date(this.temp.endDate)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp) // copy obj
          tempData.startDate = +new Date(tempData.startDate) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          tempData.endDate = +new Date(tempData.endDate) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateCurriculumData(tempData).then(response => {
            const argument = JSON.parse(response.data.return.argument)
            const message = response.data.message
            for (const v of this.list) {
              if (v.curriculumNo === argument.curriculumNo) {
                const index = this.list.indexOf(v)
                this.list.splice(index, 1, argument)
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
      })
    },
    handleDelete(row) {
      const curriculumNo = row.curriculumNo
      deleteCurriculumData(curriculumNo).then(response => {
        const message = response.data.message
        const index = this.list.indexOf(row)
        this.list.splice(index, 1)
        this.$notify({
          title: message.title,
          message: message.content,
          type: 'success',
          duration: 2000
        })
      })
    },
    handleFileSubmit(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.curriculumNo = row.curriculumNo
      this.temp.startDate = new Date(this.temp.startDate)
      this.temp.endDate = new Date(this.temp.endDate)
      this.$refs['excel-upload-input'].click()
    },
    handleFileUpload(e) {
      const files = e.target.files
      const rawFile = files[0]
      this.temp.applicantsBulkXlsxFile = rawFile
      this.createApplicantsData()
    },
    createApplicantsData() {
      createApplicantsBulk(this.temp).then(response => {
        const message = response.data.message
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
    },
    handleFileDownload(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.curriculumNo = row.curriculumNo
      this.downloadAttendanceLogsListfile()
    },
    downloadAttendanceLogsListfile() {
      const query = { curriculumNo: this.temp.curriculumNo }
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
          type: 'warn',
          duration: 2000
        })
      })
    }
  }
}
</script>

<style scoped>
.excel-upload-input{
  display: none;
  z-index: -9999;
}
</style>
