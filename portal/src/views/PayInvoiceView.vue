<template>
 
    <div class="App container mt-5">
        <h1>Pagar Factura: {{$route.params.invoiceId}}</h1>
        
        <form @submit.prevent="submitForm" encType='multipart/form-data'>
            <div class="mb-3">
                <label for="formFile" class="form-label">Cargar Comprobante:</label>
                <input class="form-control" ref="fileInput" type="file" @input="pickFile" @change="onchange">
            </div>
            <div class="imagePreviewWrapper" :style="{ 'background-image': `url(${previewImage})` }" @click="selectImage"></div>
            <button class="w-100 btn btn-lg btn-primary" type="submit">Enviar</button>
        </form>
        
    </div>
   
</template>


   <script>
   //importing bootstrap 5 and pdf maker Modules
   import "bootstrap/dist/css/bootstrap.min.css";
   import { ref } from "vue";
   import { useRoute, useRouter } from 'vue-router'
   import { BASE_API_URL } from "../main";
   export default {

        setup() {
            const route = useRoute()
            const router = useRouter();

            const file = ref("");
         
            const onchange = (e) => {
                console.log("Cambio");
                file.value = e.target.files[0];
            }      

            const submitForm = async() => {
                let invoiceId = route.params.invoiceId     

                let formData = new FormData(); 
                formData.append("invoiceId", invoiceId);
                formData.append("file", file.value);

                console.log(invoiceId)
                let response = await fetch(BASE_API_URL+'/api/me/makepayment', {
                    method: 'POST',
                    credentials: "include",
                    mode: "cors",
                    body: formData               
                });
                if (!response.ok){
                    const message = `An error has occured: ${response.status} - ${response.statusText}`;
                    throw new Error(message);
                } else {
                    await router.push("/payments");
                }
            };

            return {
                submitForm, onchange
            }
        },

       methods: {
         //image upload and preview methods
         selectImage () {
             this.$refs.fileInput.click()
         },
         pickFile () {
           let input = this.$refs.fileInput
           let file = input.files
           if (file && file[0]) {
             let reader = new FileReader
             reader.onload = e => {
               this.previewImage = e.target.result
             }
             reader.readAsDataURL(file[0])
             this.$emit('input', file[0])
           }
         }
        },
        data: function() {
            return {
                previewImage: null
            }  
        }
    }

    
    
</script>


<style>
.imagePreviewWrapper {
  background-repeat: no-repeat;
    width: 250px;
    height: 250px;
    display: block;
    cursor: pointer;
    margin: 0 auto 30px;
    background-size: contain;
    background-position: center center;
}
</style>
