import Vue from 'vue'
import VueI18n from 'vue-i18n'
import Cookies from 'js-cookie'
import elementEnLocale from 'element-ui/lib/locale/lang/en' // element-ui lang
import elementKoLocale from 'element-ui/lib/locale/lang/ko'// element-ui lang
import enLocale from './en'
import koLocale from './ko'

Vue.use(VueI18n)

const messages = {
  en: {
    ...enLocale,
    ...elementEnLocale
  },
  ko: {
    ...koLocale,
    ...elementKoLocale
  }
}

const i18n = new VueI18n({
  // set locale
  // options: en | ko
  locale: Cookies.get('language') || 'ko',
  // set locale messages
  messages
})

export default i18n
