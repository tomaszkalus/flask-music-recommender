const { createApp, ref, watch } = Vue
const { createVuetify } = Vuetify
import SongAutoCompleteInput from "./SongAutoCompleteInput.js"

const vuetify = createVuetify()

const app = createApp({

    components:{
        SongAutoCompleteInput
    },

    setup() {
        const user_songs = ref([null]);

        // let loading = ref(false);
        // let items = ref([]);
        // let search = ref(null);
        // let select = ref(null);
        // let lastExecution = Date.now();
        // const delay = 500

        // watch(search, (val) => {
        //     if (val.length == 0) { items.value.length = 0 }
        //     if (val.length > 2 && ((lastExecution + delay) < Date.now())) {
        //         val && val !== select.value && getSongsSuggestions(val)
        //         console.log(val)
        //         lastExecution = Date.now()
        //     }
        // })

        // async function getSongsSuggestions(userInput) {
        //     loading = true;
        //     const response = await fetch("/search/" + encodeURIComponent(userInput));
        //     const songs = await response.json();
        //     items.value = songs.map(e => `${e['artists']} - ${e['name']}`)
        //     console.log(songs);
        //     loading = false;
        // }

        function addSong() {
            user_songs.value.push(null);
        }

        function removeSong(index) {
            if (user_songs.value.length > 1) {
                user_songs.value.splice(index, 1);
            }
        }

        function submitForm() {

            console.log(user_songs.value)

            // const songsObj = {};

            // for (const [index, element] of user_songs.value.entries()) {
            //     songsObj['artist' + (index + 1)] = element['artist']
            //     songsObj['name' + (index + 1)] = element['name']
            // }

            // const queryString = new URLSearchParams(songsObj).toString();

            // window.location.href = "/show_recommendations?" + queryString;
        }


        return {
            user_songs,
            addSong,
            removeSong,
            submitForm,
            // loading,
            // items,
            // search,
            // select

        }
    }
})
app.use(vuetify);
// app.component('AutoComplete', AutoComplete);
app.mount('#app')