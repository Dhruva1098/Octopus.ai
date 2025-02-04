<template>
  <div class="app">
    <nav class="navbar">
      <div class="navbar-left">Octopus_AI</div>
      <div class="navbar-right">
        <button class="add-note-btn" @click="goToCreateNote">+</button>
      </div>
    </nav>

    <div class="main-content">
      <h1> Welcome to Octopus_AI</h1>
      <input
        v-model="query"
        type="text"
        class="search-bar"
        />
      <button class="ask-btn" @click="handleAsk">Ask</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',  // stores user input
    };
  },
  methods:{
    goToCreateNote(){
      alert("Navigating to creating notes page");
    },
    handleAsk(){
      alert(`You Asked: ${this.query}`);
    }
  }
}
</script>
<style>
/* General Styles */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* Navbar Styles */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-left {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.navbar-right .add-note-btn {
  background-color: #007bff;
  color: white;
  border: none;
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.navbar-right .add-note-btn:hover {
  background-color: #0056b3;
}

/* Main Content Styles */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.main-content h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.search-bar {
  width: 80%;
  max-width: 500px;
  padding: 0.8rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-bar:focus {
  border-color: #007bff;
}

.ask-btn {
  margin-top: 1rem;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.ask-btn:hover {
  background-color: #0056b3;
}
</style>
