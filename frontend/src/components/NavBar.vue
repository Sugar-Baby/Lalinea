<template>
  <v-app-bar flat color="#F3E8FF" class="lalinea-navbar">
    <v-row class="w-100" align="center" no-gutters>
      <!-- 左侧按钮 -->
      <v-col cols="auto" class="pl-6">
        <v-btn to="/" variant="text" class="font-weight-bold mr-4">Home</v-btn>
        <v-btn to="/list" variant="text">List of people and groups</v-btn>
      </v-col>
      <v-spacer />
      <!-- 右侧搜索栏和用户按钮 -->
      <v-col cols="auto" class="d-flex align-center pr-6">
        <v-text-field
          v-model="search"
          placeholder="Search..."
          density="compact"
          hide-details
          variant="outlined"
          class="mr-2"
          style="min-width: 320px; max-width: 480px;"
          @keyup.enter="onSearch"
          append-inner-icon="mdi-magnify"
          @click:append-inner="onSearch"
        />
        <v-btn
          v-if="isLoggedIn"
          to="/profile"
          variant="text"
          class="ml-2 font-weight-bold"
        >
          {{ username }}
        </v-btn>
        <v-btn
          v-else
          to="/login"
          variant="outlined"
          class="ml-2 font-weight-bold"
        >
          Log in / Sign up
        </v-btn>
      </v-col>
    </v-row>
  </v-app-bar>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const search = ref('')
const router = useRouter()

const isLoggedIn = ref(false)
const username = ref('')

function updateLoginState() {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true';
  username.value = localStorage.getItem('name') || '';
}

onMounted(() => {
  updateLoginState();
  window.addEventListener('storage', updateLoginState);
})

function onSearch() {
  if (search.value.trim()) {
    router.push(`/search?q=${encodeURIComponent(search.value.trim())}`)
  }
}
</script>

<style scoped>
.lalinea-navbar {
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
</style> 