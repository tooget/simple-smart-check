<template>
  <v-ons-page>
    <div class="camera">
      <div class="focus">

        <p class="intro">result: <b>{{ result }}</b></p>
        <qrcode-drop-zone @decode="onDecode" @init="logErrors">
          <qrcode-stream :camera="{ facingMode }" @init="onInit">
            <button @click="switchCamera">Switch Camera</button>
          </qrcode-stream>
        </qrcode-drop-zone>
        <qrcode-capture v-if="noStreamApiSupport" @decode="onDecode" />

        <p class="intro">[TEST] Fetch timestamp from the Flask server<br/>
          <a href="" @click.prevent="fetchResource">Fetch</a><br/>
          <a href="" @click.prevent="fetchSecureResource">Fetch Secure Resource</a>
        </p>
        <p class="intro" v-for="r in resources" :key="r.timestamp">
          Server Timestamp: {{r.timestamp | formatTimestamp }}
        </p>
      </div>
    </div>
  </v-ons-page>
</template>

<script>
import $backend from '../backend'

const REAR_CAMERA = { ideal: 'environment' }
const FRONT_CAMERA = { exact: 'user' }

export default {
  data () {
    return {
      resources: [],
      error: '',
      result: '',
      facingMode: REAR_CAMERA,
      noFrontCamera: false,
      noStreamApiSupport: false
    }
  },

  methods: {
    onDecode (result) {
      this.result = result
    },

    logErrors (promise) {
      promise.catch(console.error)
    },

    switchCamera () {
      if (this.facingMode === FRONT_CAMERA) {
        this.facingMode = REAR_CAMERA
      } else {
        this.facingMode = FRONT_CAMERA
      }
    },

    async onInit (promise) {
      try {
        await promise
      } catch (error) {
        if (error.name === 'StreamApiNotSupportedError') {
          this.noStreamApiSupport = true
          this.noFrontCamera = this.facingMode === FRONT_CAMERA
            && error.name === 'OverconstrainedError'

          console.error(error)
        }
      }
    },

    fetchResource () {
      $backend.fetchResource()
        .then(responseData => {
          this.resources.push(responseData)
        }).catch(error => {
          this.error = error.message
        })
    },

    fetchSecureResource () {
      $backend.fetchSecureResource()
        .then(responseData => {
          this.resources.push(responseData)
        }).catch(error => {
          this.error = error.message
        })
    }
  }
}
</script>

<style scoped>
button {
  position: absolute;
  left: 10px;
  top: 10px;
}
.camera {
  width: 100%;
  height: 100%;
  background-color: lightgrey;
  vertical-align: middle;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.focus {
  width: 100%;
  height: 100%;
}
</style>



