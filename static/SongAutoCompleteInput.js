const { ref, watch, emit } = Vue

export default {
    name: 'SongAutoCompleteInput',

    props: {
        selected: String
    },

    setup(props, { emit }){
        let loading = ref(false);
        let items = ref([]);
        let search = ref(null);
        let select = ref(null);
        let lastExecution = Date.now();
        const delay = 500


        watch(search, (val) => {
            if (val.length == 0) { items.value.length = 0 }
            if (val.length > 2 && ((lastExecution + delay) < Date.now())) {
                val && val !== select.value && getSongsSuggestions(val)
                lastExecution = Date.now()
            }        
        })

        watch(select, (val) => {
            emit('selectedchanged', val);
            console.log(`Selected value: ${val}`)
        })

        async function getSongsSuggestions(userInput) {
            loading = true;
            const response = await fetch("/search/" + encodeURIComponent(userInput));
            const suggestedSongs = await response.json();
            items.value = suggestedSongs.map(song => ({ artists: song.artists, name: song.name, id: song.id }));
            // console.log(suggestedSongs)

            loading = false;
        }

        return {
            loading,
            items,
            search,
            select
        }

    },

    template: `
    <v-autocomplete
            class="user-song-input"
            v-model="select"
            v-model:search="search"
            :loading="loading"
            :items="items"
            no-filter
            item-title="name"
            item-value="id"
            @update:focused="(v) => {}"
            density="comfortable"
            hide-no-data
            hide-details
            label="Enter song for recommendation">

            <template v-slot:item="{ props, item }">
                <v-list-item
                  v-bind="props"
                  :title="item.raw.name"
                  :subtitle="item.raw.artists"
                ></v-list-item>
              </template>
            
            
            </v-autocomplete>
    `
  }
  