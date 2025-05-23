<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Register</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="studentId"
                label="Student ID"
                name="studentId"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>

              <v-text-field
                v-model="email"
                label="Email"
                name="email"
                prepend-icon="mdi-email"
                type="email"
                required
              ></v-text-field>

              <v-text-field
                v-model="name"
                label="Name"
                name="name"
                prepend-icon="mdi-account-box"
                type="text"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>

              <v-text-field
                v-model="contact"
                label="Contact (optional)"
                name="contact"
                prepend-icon="mdi-phone"
                type="text"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions class="justify-center pb-4">
            <v-btn
              color="primary"
              size="large"
              min-width="200"
              elevation="2"
              :loading="loading"
              :disabled="loading"
              @click="handleRegister"
            >
              Register
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            Already have an account?
            <a
              href="#"
              class="text-decoration-none register-link"
              @click.prevent="goToLogin"
            >
              Login here
            </a>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from '@/utils/axios';

const router = useRouter();
const studentId = ref('');
const email = ref('');
const name = ref('');
const password = ref('');
const contact = ref('');
const loading = ref(false);

const handleRegister = async () => {
  if (!studentId.value || !email.value || !name.value || !password.value) {
    alert('请填写所有必填字段');
    return;
  }
  try {
    loading.value = true;
    const response = await axios.post('/register', {
      student_id: studentId.value,
      email: email.value,
      name: name.value,
      password: password.value,
      contact: contact.value
    });
    if (response.data.message === '注册成功') {
      alert('注册成功！请登录');
      router.push('/login');
    }
  } catch (error) {
    if (error.response) {
      alert(`注册失败：${error.response.data.error || '请重试'}`);
    } else {
      alert('注册失败，请检查网络连接');
    }
  } finally {
    loading.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
.register-link {
  color: var(--v-theme-primary);
}
</style> 