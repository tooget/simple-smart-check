 <template>   
    <v-ons-page>
      <custom-toolbar backLabel="Back">
        {{ item.curriculumName }}
      </custom-toolbar>

      <v-ons-list>
        <v-ons-list-header>Class Information</v-ons-list-header>
        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <div class="left">
            curriculumCategory:
          </div>
          <label class="center">
            {{ item.curriculumCategory }}
          </label>
        </v-ons-list-item>

        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <div class="left">
            ordinalNo:
          </div>
          <div class="center">
            {{ item.ordinalNo }}
          </div>
        </v-ons-list-item>

        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <div class="left">
            curriculumName:
          </div>
          <div class="center">
            {{ item.curriculumName }}
          </div>
        </v-ons-list-item>

        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <div class="left">
            curriculumType:
          </div>
          <div class="center">
            {{ item.curriculumType }}
          </div>
        </v-ons-list-item>

        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <div class="left">
            startDate:
          </div>
          <div class="center">
            {{ item.startDate }}
          </div>
        </v-ons-list-item>

        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <div class="left">
            endDate:
          </div>
          <div class="center">
            {{ item.endDate }}
          </div>
        </v-ons-list-item>

        <v-ons-list-header>phoneNo</v-ons-list-header>
        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <div class="left">
            phoneNo:
          </div>
          <label class="center">
            <v-ons-input float maxlength="20"
              placeholder="phoneNo"
              v-model="phoneNo"
            >
            </v-ons-input>
          </label>
        </v-ons-list-item>

        <v-ons-list-header>attendanceType</v-ons-list-header>
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
            {{ attendanceType }}
          </label>
        </v-ons-list-item>

        <v-ons-list-header>signaturePad</v-ons-list-header>
        <v-ons-list-item :modifier="md ? 'nodivider' : ''">
          <div class="left">
            signaturePad:
          </div>
          <label class="center">
            <div class="col-12 mt-2">
              <VueSignaturePad
                id="signature"
                width="100%"
                height="500px"
                ref="signaturePad"
              />
            </div>
            <div class="col-6 mt-2">
              <button
                class="btn btn-outline-secondary float-right"
                @click="undo"
              >
                Undo
              </button>
            </div>
            <div class="col-6 mt-2">
              <button
                class="btn btn-outline-primary float-left"
                @click="save"
              >
                Save
              </button>
            </div>
          </label>
        </v-ons-list-item>

      </v-ons-list>
    </v-ons-page>
</template>

<script>
export default {
  computed: {
    checkInOut () {
      return this.$store.state.attendanceLog.status.checkInOut;
    }
  },
  methods: {
    undo() {
      this.$refs.signaturePad.undoSignature();
    },
    save() {
      const { isEmpty, data } = this.$refs.signaturePad.saveSignature();
      const { dispatch } = this.$store;
      const requestBody = {
        phoneNo: this.phoneNo,
        curriculumNo: this.item.curriculumNo,
        checkInOut: this.selectAttendanceType,
        signature: data
      };
      dispatch('attendanceLog/checkInOut', { requestBody });
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