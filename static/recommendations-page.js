const { createApp, ref } = Vue
const { createVuetify } = Vuetify

const vuetify = createVuetify()

const app = createApp({

    setup() {
        const expand = ref(false)
        const time = ref(0)
        
        return {
            expand,
            time
        }
    }
})
app.use(vuetify);
app.mount('#app')