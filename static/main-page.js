const { createApp, ref } = Vue
const { createVuetify } = Vuetify
import SongAutoCompleteInput from "./SongAutoCompleteInput.js"

const vuetify = createVuetify()

const app = createApp({

    components: {
        SongAutoCompleteInput
    },

    setup() {
        const user_songs = ref([null]);

        function addSong() {
            user_songs.value.push(null);
        }

        function removeSong(index) {
            if (user_songs.value.length > 1) {
                user_songs.value.splice(index, 1);
            }
        }

        function submitForm() {

            const songsObj = {};
            console.log(user_songs.value)
            // console.log(SongIds)

            // for (const [index, element] of user_songs.value.entries()) {
            //     songsObj['artist' + (index + 1)] = element['artists']
            //     songsObj['name' + (index + 1)] = element['name']
            // }

            for (const [index, element] of user_songs.value.entries()) {
                songsObj['id' + (index + 1)] = element['id']
            }

            const queryString = new URLSearchParams(songsObj).toString();
            window.location.href = "/show_recommendations?" + queryString;
        }

        return {
            user_songs,
            addSong,
            removeSong,
            submitForm,
        }
    }
})
app.use(vuetify);
app.mount('#app')