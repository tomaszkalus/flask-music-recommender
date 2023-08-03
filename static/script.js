const { createApp, ref } = Vue

const app = createApp({
    setup() {
        const user_songs = ref([{ artist: "Arctic Monkeys", name: "R U Mine?" }]);

        function addSong() {
            user_songs.value.push({ artist: "", name: "" });
        }

        function removeSong(index) {
            if (user_songs.value.length > 1) {
                user_songs.value.splice(index, 1);
            }
        }

        function submitForm() {
            const songsObj = {};

            for (const [index, element] of user_songs.value.entries()) {
                songsObj['artist' + (index + 1)] = element['artist']
                songsObj['name' + (index + 1)] = element['name']
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
app.mount('#app')