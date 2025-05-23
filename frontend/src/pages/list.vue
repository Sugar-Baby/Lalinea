<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="mb-6">所有标签</h1>
      </v-col>
      <v-col
        v-for="hobby in hobbies"
        :key="hobby.id"
        cols="12" sm="6" md="4" lg="3"
      >
        <v-card class="hobby-card" @click="goToCircle(hobby.id)" hover>
          <v-card-title>{{ hobby.name }}</v-card-title>
          <v-card-subtitle>人数：{{ hobby.user_count }}</v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/utils/axios';
import { useRouter } from 'vue-router';

const hobbies = ref([]);
const router = useRouter();

const fetchHobbies = async () => {
  const res = await axios.get('/api/hobbies');
  hobbies.value = res.data;
};

const goToCircle = (id) => {
  router.push(`/circle?id=${id}`);
};

onMounted(fetchHobbies);
</script>

<style scoped>
.hobby-card {
  cursor: pointer;
  border: 1.5px solid #A084CA;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.hobby-card:hover {
  border-color: #7C5DA8;
  box-shadow: 0 4px 16px rgba(160, 132, 202, 0.15);
}
</style> 