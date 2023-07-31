export default {
  template: `
  <h2 style="color: red">Recommendations</h2>
  `,
  method: {
    changeStep(){
       this.$emit("nextStep", "SongsInput");
    }
 }
}
