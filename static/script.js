document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("songs-selection");
    addNewSongSelection()

    const newSongBtn = document.querySelector('#add-new-song');

    newSongBtn.addEventListener("click", () => {
      addNewSongSelection();

    })
  
    form.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent default form submission
  
      // Get form data and create a FormData object
      const formData = new FormData(form);

      const songs = getSongsList();
      const songsJson = JSON.stringify(songs);

      // const params = new URLSearchParams(songs).toString();

      // console.log(params)

  
      // Send the data to the endpoint using the fetch API
      fetch(form.action, {
        method: "POST",
        body: songsJson,
        headers: {
            "Content-Type": "application/json",
          }
      })
        .then((response) => response.json()) // If expecting JSON response
        .then((data) => {
          console.log(data);
        })
        .catch((error) => {
          // Handle any errors that occurred during the fetch
          console.error("Error:", error);
        });

    });
  });

  function addNewSongSelection(){
    const template = document.querySelector('#song-selection-template');
    const songSelectorsContainer = document.querySelector('#songs-selectors');
    const songSelectorNode = template.content.cloneNode(true);
    songSelectorsContainer.appendChild(songSelectorNode);

    const lastSongSelector = songSelectorsContainer.lastElementChild;
    const removeSongBtn = lastSongSelector.querySelector('.delete-song-button');

    removeSongBtn.addEventListener('click', () => {
      lastSongSelector.remove();
    })

  }

  function getSongsList(){
    const songSelectorsContainer = document.querySelector('#songs-selectors');
    const songSelectors = songSelectorsContainer.children;
    songs = [];

    for (let songSelector of songSelectors) {
      const artist = songSelector.querySelectorAll('.artist-textbox')[0].value
      const name = songSelector.querySelectorAll('.title-textbox')[0].value
      const song = {artist, name};
      songs.push(song);

    } 
    return songs;



  }


