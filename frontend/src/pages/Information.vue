<template>
  <v-ons-page>

    <v-ons-list>
      <v-ons-list-header>Version</v-ons-list-header>
      <v-ons-list-item :modifier="md ? 'nodivider' : ''">
        v0.0.1
      </v-ons-list-item>

      <v-ons-list-header>Volume</v-ons-list-header>
      <v-ons-list-item>
        Adjust the volume:
        <v-ons-row>
          <v-ons-col width="40px" style="text-align: center; line-height: 31px;">
            <v-ons-icon icon="md-volume-down"></v-ons-icon>
          </v-ons-col>
          <v-ons-col>

            <v-ons-range v-model="volume" style="width: 100%;"></v-ons-range>

          </v-ons-col>
          <v-ons-col width="40px" style="text-align: center; line-height: 31px;">
            <v-ons-icon icon="md-volume-up"></v-ons-icon>
          </v-ons-col>
        </v-ons-row>
        Volume: {{ volume }} <span v-show="Number(volume) > 80">&nbsp;(careful, that's loud)</span>
      </v-ons-list-item>

      <v-ons-list-header>Alarm</v-ons-list-header>
      <ons-list-item>
        <label class="center" for="switch1">
          Total ({{ switchOn ? 'on' : 'off' }})
        </label>
        <div class="right">
          <v-ons-switch input-id="switch1" v-model="switchOn">
          </v-ons-switch>
        </div>
      </ons-list-item>
      <ons-list-item>
        <label class="center" for="switch2">
          {{ switchOn ? 'Enabled alarm' : 'Disabled alarm' }}
        </label>
        <div class="right">
          <v-ons-switch input-id="switch2" :disabled="!switchOn">
          </v-ons-switch>
        </div>
      </ons-list-item>

      <v-ons-list-header>Mode</v-ons-list-header>
      <v-ons-list-item v-for="(mode, $index) in modes" :key="mode"
        tappable
        :modifier="($index === modes.length - 1) ? 'longdivider' : ''"
      >
        <label class="left">
          <v-ons-radio
            :input-id="'radio-' + $index"
            :value="mode"
            v-model=" selectedMode"
          >
          </v-ons-radio>
        </label>
        <label :for="'radio-' + $index" class="center">
          {{ mode }}
        </label>
      </v-ons-list-item>
      <v-ons-list-item>
        <div class="center">
          I love {{ selectedMode }}!
        </div>
      </v-ons-list-item>

    </v-ons-list>
  </v-ons-page>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      switchOn: true,
      selectedMode: 'Active',
      modes: ['Active', 'Hibernate', 'Dev'],
      volume: 25
    };
  }
};
</script>

<style scoped>
.right-icon {
  margin-left: 10px;
}
.right-label {
  color: #666;
}
</style>
