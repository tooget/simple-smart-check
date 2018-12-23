<template>
  <v-ons-page>
    <p class="intro">
      Input Class Name &amp; Email address to create NEW CLASS.<br><br>
    </p>

    <v-ons-card>
      <div class="card__item">
        <div class="card__item__left">
          <v-ons-icon icon="ion-checkmark" class="list-item__icon"></v-ons-icon>
        </div>
        <label class="card__item__center">
          <v-ons-input float maxlength="30"
            placeholder="Class Name"
            v-model="className"
          >
          </v-ons-input>
        </label>
      </div>

      <div class="card__item">
        <div class="card__item__left">
          <v-ons-icon icon="ion-checkmark" class="list-item__icon"></v-ons-icon>
        </div>
        <label class="card__item__center">
          <v-ons-input float maxlength="30"
            placeholder="Organizer's Email"
            v-model="email"
          >
          </v-ons-input>
        </label>
      </div>

      <p style="text-align: center">
        <v-ons-button @click="dialogVisible = true">
          CREATE
        </v-ons-button>
      </p>

      <v-ons-dialog
        cancelable
        :visible.sync="dialogVisible"
      >
        <v-ons-card>
          <qrcode-vue style="text-align: center" :value="className" :size="size" level="H"></qrcode-vue>
          <div class="card__title">Class Name:</div> 
          <div>{{className}}</div> 
          
          <div class="card__title">Organizer's Email:</div>
          <div>{{email}}</div>
          
          <p style="text-align: center">
            <v-ons-button @click.prevent="fetchSecureResourceContract">
              CONFIRM
            </v-ons-button>
          </p>
        </v-ons-card>
      </v-ons-dialog>

    </v-ons-card>
  </v-ons-page>
</template>

<script>
import QrcodeVue from 'qrcode.vue';
import $backend from '../backend'

export default {
  data () {
    return {
      className: '',
      email: '',
      dialogVisible: false,
      size: 150
    };
  },

  methods: {
    fetchSecureResourceContract () {
      $backend.fetchSecureResourceContract(this.email, this.className)
        .then(responseData => {
          this.resources.push(responseData)
        }).catch(error => {
          this.error = error.message
        })
      this.dialogVisible = false  
    }
  },

  components: {
    QrcodeVue
  }
}
</script>

<style>
.intro {
  text-align: left;
  padding: 0 22px;
  margin-top: 20px;
  font-size: 14px;
  line-height: 1.4;
  color: rgba(0, 0, 0, .54);
}

ons-card {
  width: 96%;
  height: 60%;
  cursor: pointer;
  color: #333;
}

.card__item {
  padding: 0 22px;
  margin-top: 25px;
  margin-bottom: 25px;
}

.card__title, .card--material__title {
  font-size: 14px;
}

.card__item__left {
    float:left;
    margin:0 10px;
}

.card__item__center {
    display: inline-block;
    margin: 0 20px;
    width: 200px;
}

</style>
