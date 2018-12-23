<template>
  <v-ons-page>
    <p class="intro">
      Input your Email address to check the state of Class or Participation.<br><br>
    </p>

    <v-ons-card>
      <div class="card__item">
        <div class="card__item__left">
          <v-ons-icon icon="ion-checkmark" class="list-item__icon"></v-ons-icon>
        </div>
        <label class="card__item__center">
          <v-ons-input float maxlength="20"
            placeholder="Email address"
            v-model="name"
          >
          </v-ons-input>
        </label>
      </div>
      <p style="text-align: center">
        <v-ons-button>CREATE</v-ons-button>
      </p>
    </v-ons-card>
  </v-ons-page>
</template>

<script>
export default {
  data () {
    return {
      name: ''
    };
  },
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
  vertical-align: middle;
  cursor: pointer;
  color: #333;
}

.card__item {
  padding: 0 22px;
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
    margin:0 20px;
    width:200px;
}
</style>
