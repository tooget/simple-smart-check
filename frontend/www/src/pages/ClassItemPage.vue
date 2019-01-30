 <template>   
    <v-ons-page>
      <custom-toolbar backLabel="Back">
        {{ item.curriculumName +' '+ item.ordinalNo +' ('+ item.startDate +'~'+ item.endDate +')' }}
      </custom-toolbar>

      <v-ons-list>
        <v-ons-list-header>전화번호</v-ons-list-header>
        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <div class="left">
            <v-ons-icon icon="ion-ios-telephone" class="list-item__icon"></v-ons-icon>
          </div>
          <label class="center">
            <v-ons-input float maxlength="20"
              placeholder="ex) 010-1234-5678"
              v-model="phoneNo"
            >
            </v-ons-input>
          </label>
        </v-ons-list-item>

        <v-ons-list-header>입실/퇴실 여부</v-ons-list-header>
        <v-ons-list-item v-for="(attendanceType, $index) in attendanceTypes" :key="attendanceType"
          tappable
          :modifier="($index === attendanceTypes.length - 1) ? 'longdivider' : ''"
        >
          <label class="left">
            <v-ons-radio
              :input-id="'radio-' + $index"
              :value="attendanceType"
              v-model=" selectAttendanceType"
            >
            </v-ons-radio>
          </label>
          <label :for="'radio-' + $index" class="center">
            {{ attendanceType | attendanceTypeFilter }}
          </label>
        </v-ons-list-item>

        <v-ons-list-header>서명</v-ons-list-header>
        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <label class="center">
            <div class="col-12 mt-2" align="center">
              <VueSignaturePad
                id="signature"
                width="480px"
                height="360px"
                ref="signaturePad"
                :options="{ 
                  dotSize: (2 + 3) / 2,
                  minWidth: 2,
                  maxWidth: 3,
                  throttle: 16,
                  minDistance: 5,
                  backgroundColor: 'rgba(0,0,0,0)',
                  penColor: 'black',
                  velocityFilterWeight: 0.8 
                }"
              />
            </div>
            <div class="col-6 mt-2">
              <ons-button
                class="btn btn-outline-secondary float-right"
                @click="clear"
              >
                재서명
              </ons-button>
            </div>
            <div class="col-6 mt-2">
              <ons-button
                class="btn btn-outline-primary float-left"
                @click="handleSubmit"
              >
                출석확인
              </ons-button>
            </div>
          </label>
        </v-ons-list-item>

      </v-ons-list>
    </v-ons-page>
</template>

<script>
export default {
  filters: {
    attendanceTypeFilter(status) {
      const statusMap = {
        In: '입실',
        Out: '퇴실'
      }
      return statusMap[status]
    }
  },
  computed: {
    checkInOut () {
      return this.$store.state.attendanceLog.status.checkInOut;
    }
  },
  methods: {
    clear() {
      this.$refs.signaturePad.clearSignature();
    },
    handleSubmit (e) {
      const { isEmpty, data } = this.$refs.signaturePad.saveSignature();
      const { dispatch } = this.$store;
      const phoneNo = this.phoneNo;
      const curriculumNo = this.item.curriculumNo;
      const checkInOut = this.selectAttendanceType;
      const signature = data;
      dispatch('attendanceLog/checkInOut', { phoneNo, curriculumNo, checkInOut, signature }
        ).then(response => {
          const message = response.data.message;
          this.$ons.notification.toast(message.title +', '+ message.content, {timeout: 3000});
          this.phoneNo = null;
          this.selectAttendanceType = undefined;
          this.$refs.signaturePad.clearSignature();
        }).catch(error => {
          const message = error.response.data.message;
          this.$ons.notification.alert(message.title +', '+ message.content);
        })
    }
  }
};
</script>

<style>
#signature {
  border: double 3px transparent;
  border-radius: 5px;
  background-image: linear-gradient(white, white),
    radial-gradient(circle at top left, #4bc5e8, #9f6274);
  background-origin: border-box;
  background-clip: content-box, border-box;
}
</style>