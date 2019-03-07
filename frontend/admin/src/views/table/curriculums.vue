<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input :placeholder="$t('table.curriculums.curriculumName')" v-model="listQuery.curriculumName" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-button v-waves :loading="listLoading" class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">{{ $t('table.search') }}</el-button>
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
      <el-table-column :label="$t('table.curriculums.curriculumNo')" prop="curriculumNo" sortable="custom" width="85px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node.curriculumNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.curriculumName')" prop="curriculumName" sortable="custom" width="255px" align="center">
        <template slot-scope="scope">
          <span class="link-type" @click="handleUpdate(scope.row)">{{ scope.row.node.curriculumName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.ordinalNo')" prop="ordinalNo" sortable="custom" width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node.ordinalNo }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.curriculumCategory')" prop="curriculumCategory" sortable="custom" width="140px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node.curriculumCategory }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.curriculumType')" prop="curriculumType" sortable="custom" width="120px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node.curriculumType }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.startDate')" prop="startDate" sortable="custom" width="110px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node.startDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.endDate')" prop="endDate" sortable="custom" width="110px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node.endDate | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showApplicantsBulkInserted" :label="$t('table.curriculums.applicantsBulkInserted')" width="150px" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <input ref="excel-upload-input" class="excel-upload-input" type="file" accept=".xlsx, .xls" @change="handleFileUpload">
          <el-button :loading="uploadExcelLoading" size="mini" type="primary" @click="handleFileSubmit(scope.row)">{{ $t('table.browse') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="showDonwnloadAtendanceLogs" :label="$t('table.curriculums.donwnloadAtendanceLogs')" width="150px" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button v-waves :loading="downloadLoading" size="mini" type="primary" @click="handleFileDownload(scope.row)">{{ $t('table.download') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="showDelete" :label="$t('table.curriculums.delete')" width="150px" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">{{ $t('table.delete') }}</el-button>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.insertedTimestamp')" prop="insertedTimestamp" sortable="custom" width="175px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node.insertedTimestamp | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.curriculums.updatedTimestamp')" prop="updatedTimestamp" sortable="custom" width="175px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node.updatedTimestamp | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="pagenum" :limit.sync="listQuery.first" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="150px" style="width: 450px; margin-left:50px;">
        <el-form-item :label="$t('table.curriculums.curriculumName')" prop="curriculumName">
          <el-input v-model="temp.curriculumName" :placeholder="$t('table.curriculums.curriculumName')"/>
        </el-form-item>
        <el-form-item :label="$t('table.curriculums.ordinalNo')" prop="ordinalNo">
          <el-input v-model="temp.ordinalNo" :placeholder="$t('table.curriculums.ordinalNo')"/>
        </el-form-item>
        <el-form-item :label="$t('table.curriculums.curriculumCategory')" prop="curriculumCategory">
          <el-input v-model="temp.curriculumCategory" :placeholder="$t('table.curriculums.curriculumCategory')"/>
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
import { fetchCurriculumsListGql, createCurriculumsData, updateCurriculumsData, deleteCurriculumsData } from '@/api/resource/curriculums'
import { createApplicantsBulk } from '@/api/resource/applicants'
import { fetchAttendanceLogsListfile } from '@/api/resource/attendanceLogs'
import waves from '@/directive/waves' // Waves directive
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      pagenum: 1,
      downloadLoading: false,
      listLoading: true,
      listQuery: {
        first: 20,
        after: '',
        order: 'curriculumNo_desc',
        curriculumName: '',
        curriculumCategory: ''
      },
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
        update: '수정',
        create: '입력'
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
      const listIndex = ((this.pagenum - 1) * this.listQuery.first)
      if (this.list === null || listIndex === 0) {
        this.listQuery.after = ''
      } else {
        this.listQuery.after = this.list[listIndex - 1].cursor
      }
      fetchCurriculumsListGql(this.listQuery).then(response => {
        const message = JSON.parse(response.data.allCurriculums.message)
        this.list = response.data.allCurriculums.edges
        this.total = response.data.allCurriculums.totalCount

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
    handleFilter() {
      this.listQuery.after = ''
      this.getList()
    },
    sortChange(data) {
      const { prop, order } = data
      const sortOption = { ascending: 'asc', descending: 'desc' }
      this.listQuery.order = prop + '_' + sortOption[order]
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
          const timezoneOffset = new Date().getTimezoneOffset()
          const timezoneSeoul = 9 * 60 * 60 * 1000
          tempData.startDate = tempData.startDate.setHours(10, 0, 0, 0)
          tempData.endDate = tempData.endDate.setHours(18, 0, 0, 0)
          tempData.startDate = +new Date(tempData.startDate + (timezoneOffset * 60 * 1000) + timezoneSeoul) / 1000.0
          tempData.endDate = +new Date(tempData.endDate + (timezoneOffset * 60 * 1000) + timezoneSeoul) / 1000.0
          createCurriculumsData(tempData).then(response => {
            const argument = { node: response.data.createCurriculumsData.result }
            const message = JSON.parse(response.data.createCurriculumsData.message)
            this.list.unshift(argument)
            this.dialogFormVisible = false
            this.$notify({
              title: message.title,
              message: message.content,
              type: 'success',
              duration: 2000
            })
          }).catch(error => {
            const message = error.graphQLErrors[0].message
            this.$notify({
              title: message.title,
              message: message.content,
              type: 'error',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row.node) // copy obj
      this.temp.curriculumNo = parseInt(row.node.curriculumNo)
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
          const timezoneOffset = new Date().getTimezoneOffset()
          const timezoneSeoul = 9 * 60 * 60 * 1000
          tempData.startDate = tempData.startDate.setHours(10, 0, 0, 0)
          tempData.endDate = tempData.endDate.setHours(18, 0, 0, 0)
          tempData.startDate = +new Date(tempData.startDate + (timezoneOffset * 60 * 1000) + timezoneSeoul) / 1000.0
          tempData.endDate = +new Date(tempData.endDate + (timezoneOffset * 60 * 1000) + timezoneSeoul) / 1000.0
          updateCurriculumsData(tempData).then(response => {
            const argument = { node: response.data.createCurriculumsData.result }
            const message = JSON.parse(response.data.createCurriculumsData.message)
            for (const v of this.list) {
              if (v.node.curriculumNo === argument.node.curriculumNo) {
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
            const message = error.graphQLErrors[0].message
            this.$notify({
              title: message.title,
              message: message.content,
              type: 'error',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row) {
      const curriculumNo = row.curriculumNo
      deleteCurriculumsData(curriculumNo).then(response => {
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
      this.$refs['excel-upload-input'].click()
    },
    handleFileUpload(e) {
      const files = e.target.files
      const rawFile = files[0]
      this.temp.applicantsBulkXlsxFile = rawFile
      this.createApplicantsData()
    },
    createApplicantsData() {
      const data = {
        curriculumNo: this.temp.curriculumNo,
        applicantsBulkXlsxFile: this.temp.applicantsBulkXlsxFile
      }
      createApplicantsBulk(data).then(response => {
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
          title: '성공',
          message: '수강생 명단 엑셀파일을 성공적으로 다운로드하였습니다.',
          type: 'success',
          duration: 2000
        })
      }).catch(() => {
        this.$notify({
          title: '실패',
          message: '수강생 명단 엑셀파일 다운로드에 실패하였습니다.',
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
