const { createApp, ref, computed } = Vue
const { createVuetify } = Vuetify
import SongAutoCompleteInput from "./SongAutoCompleteInput.js"

const vuetify = createVuetify()

const app = createApp({

    components: {
        SongAutoCompleteInput
    },

    setup() {
        const user_songs_limit = 10;

        const user_songs = ref([null]);
        let emptyInputModal = ref(false)
        let recommendationsLoading = ref(false)

        let is_songs_limit_exceeded = computed(() => {
            return user_songs.value.length >= user_songs_limit
        })

        function addSong() {
            if (!is_songs_limit_exceeded.value) {
                user_songs.value.push(null);
            }

        }

        function removeSong(index) {
            if (user_songs.value.length > 1) {
                user_songs.value.splice(index, 1);
            }
        }

        function areInputsEmpty() {
            return user_songs.value.every(el => {
                return el == null
            })
        }

        function submitForm() {

            if (areInputsEmpty()) {
                emptyInputModal.value = true;
                return
            }

            recommendationsLoading.value = true;

            const songsObj = {};
            for (const [index, element] of user_songs.value.entries()) {
                if (element['id']) {
                    songsObj['id' + (index + 1)] = element['id']
                }

            }

            const queryString = new URLSearchParams(songsObj).toString();
            window.location.href = "/recommendations?" + queryString;
        }

        return {
            user_songs,
            addSong,
            removeSong,
            submitForm,
            is_songs_limit_exceeded,
            emptyInputModal,
            recommendationsLoading
        }
    }
})
app.use(vuetify);
app.mount('#app')