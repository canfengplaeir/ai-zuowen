<template>
  <div id="app">
    <h1>AI 作文批改系统</h1>
    <input type="file" @change="handleFileUpload" accept="image/*" />
    <button @click="submitEssay">提交作文</button>
    <div v-if="correction">
      <h2>批改结果:</h2>
      <pre>{{ correction }}</pre>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-undef */
export default {
  data() {
    return {
      file: null,
      correction: null
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async submitEssay() {
      if (!this.file) {
        alert('请选择一个图像文件');
        return;
      }

      const formData = new FormData();
      formData.append('image', this.file);

      try {
        const response = await axios.post('http://127.0.0.1:5001/api/correct', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.correction = response.data.correction;
      } catch (error) {
        console.error('Error:', error);
        alert('上传失败，请重试');
      }
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

input[type="file"] {
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: #f9f9f9;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-top: 20px;
}
</style>