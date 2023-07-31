export default {
    template: `
    <h2 style="color: red">SongsInput</h2>
    `,
    method: {
      changeStep(){
         this.$emit("nextStep", "Recommendations");
      }
   }
  }
  