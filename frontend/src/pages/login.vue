<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="studentId"
                label="Student ID"
                name="studentId"
                prepend-icon="mdi-account"
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
            </v-form>
          </v-card-text>
          <v-card-actions class="justify-center pb-4">
            <v-btn
              color="primary"
              size="large"
              min-width="200"
              elevation="2"
              :loading="isLoading"
              :disabled="isLoading"
              @click="handleLogin"
            >
              Login
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            Don't have an account?
            <a
              href="#"
              class="text-decoration-none register-link"
              @click.prevent="goToRegister"
            >
              Register here
            </a>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from '@/utils/axios';

const router = useRouter();
const studentId = ref('');
const password = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
  if (!studentId.value || !password.value) {
    alert('请填写所有必填字段');
    return;
  }
  try {
    isLoading.value = true;
    const response = await axios.post('/login', {
      student_id: studentId.value,
      password: password.value
    });
    if (response.data.message === '登录成功') {
      localStorage.clear();
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('studentId', studentId.value);
      if (response.data.name) {
        localStorage.setItem('name', response.data.name);
      }
      window.dispatchEvent(new Event('loginStateChanged'));
      alert('登录成功！');
      router.replace('/');
      // 监听路由变化，在到达首页后刷新
      const unwatch = router.afterEach((to) => {
        if (to.path === '/') {
          window.location.reload();
          unwatch(); // 移除监听器
        }
      });
    } else {
      alert('登录失败，请检查学号和密码');
    }
  } catch (error) {
    alert('登录失败，请重试');
  } finally {
    isLoading.value = false;
  }
};

const goToRegister = () => {
  router.push('/register');
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