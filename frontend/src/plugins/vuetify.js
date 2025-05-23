/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#A084CA',
          secondary: '#F7A4B8',
          accent: '#F6E7D8',
          background: '#FAF6FF',
          surface: '#FAF6FF',
          'on-surface': '#3D3759',
          'on-background': '#3D3759',
          // 你可以根据需要添加更多变量
        },
      },
    },
  },
})
