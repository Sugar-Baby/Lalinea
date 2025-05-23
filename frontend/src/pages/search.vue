<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="mb-6">搜索结果: {{ searchQuery }}</h1>
      </v-col>
      
      <!-- 圈子搜索结果 -->
      <v-col cols="12">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-title>
              相关圈子 ({{ hobbyResults.length }})
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-row>
                <v-col
                  v-for="hobby in hobbyResults"
                  :key="hobby.id"
                  cols="12"
                  md="6"
                  lg="4"
                >
                  <v-card
                    class="hobby-card"
                    @click="goToCircle(hobby.id)"
                  >
                    <v-card-text>
                      <h3 class="text-h6 mb-2">{{ hobby.name }}</h3>
                      <p class="text-subtitle-2 mb-1">
                        成员数：{{ hobby.user_count }}
                      </p>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>

      <!-- 用户搜索结果 -->
      <v-col cols="12">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-title>
              相关用户 ({{ userResults.length }})
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-row>
                <v-col
                  v-for="user in userResults"
                  :key="user.id"
                  cols="12"
                  md="6"
                  lg="4"
                >
                  <v-card class="user-card">
                    <v-card-text>
                      <div class="d-flex justify-space-between align-center">
                        <div>
                          <h3 class="text-h6 mb-2">{{ user.name }}</h3>
                          <p class="text-subtitle-2 mb-1">学号：{{ user.student_id }}</p>
                          <p v-if="user.contact" class="text-subtitle-2 mb-1">
                            联系方式：{{ user.contact }}
                          </p>
                          <p v-if="isLoggedIn" class="text-subtitle-2">
                            相似度：{{ (user.compatibility_score * 100).toFixed(1) }}%
                          </p>
                        </div>
                        <v-switch
                          v-if="isLoggedIn"
                          v-model="user.is_friend"
                          :loading="user.loading"
                          color="primary"
                          :label="user.is_friend ? '解除关系' : '我认识'"
                          @change="toggleFriendship(user)"
                          hide-details
                        ></v-switch>
                        <v-btn
                          v-else
                          color="primary"
                          variant="text"
                          @click="goToLogin"
                        >
                          登录后添加好友
                        </v-btn>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/utils/axios';

const route = useRoute();
const router = useRouter();
const searchQuery = ref('');
const hobbyResults = ref([]);
const userResults = ref([]);
const isLoggedIn = ref(false);

const checkLoginStatus = () => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true';
};

const search = async () => {
  try {
    // 搜索爱好
    const hobbyResponse = await axios.get(`/api/hobbies/search?q=${encodeURIComponent(searchQuery.value)}`);
    hobbyResults.value = hobbyResponse.data;

    // 搜索用户
    const userResponse = await axios.get(`/api/users/search?q=${encodeURIComponent(searchQuery.value)}`);
    userResults.value = userResponse.data.map(user => ({
      ...user,
      loading: false
    }));
  } catch (error) {
    console.error('Error searching:', error);
  }
};

const goToCircle = (hobbyId) => {
  router.push(`/circle?id=${hobbyId}`);
};

const goToLogin = () => {
  router.push('/login');
};

const toggleFriendship = async (user) => {
  if (!isLoggedIn.value) {
    goToLogin();
    return;
  }
  
  user.loading = true;
  try {
    if (user.is_friend) {
      // 添加好友关系
      await axios.post(`/api/user/me/friends/${user.id}`);
    } else {
      // 删除好友关系
      await axios.delete(`/api/user/me/friends/${user.id}`);
    }
    // 重新搜索以更新兼容性分数
    await search();
  } catch (error) {
    console.error('Error toggling friendship:', error);
    // 恢复开关状态
    user.is_friend = !user.is_friend;
  } finally {
    user.loading = false;
  }
};

// 监听登录状态变化
onMounted(() => {
  checkLoginStatus();
  searchQuery.value = route.query.q || '';
  if (searchQuery.value) {
    search();
  }
  
  // 添加登录状态变化监听器
  window.addEventListener('loginStateChanged', checkLoginStatus);
  window.addEventListener('storage', checkLoginStatus);
});

// 组件卸载时移除监听器
onUnmounted(() => {
  window.removeEventListener('loginStateChanged', checkLoginStatus);
  window.removeEventListener('storage', checkLoginStatus);
});
</script>

<style scoped>
.hobby-card {
  border: 1.5px solid #A084CA;
  transition: box-shadow 0.2s, border-color 0.2s;
  cursor: pointer;
}

.hobby-card:hover {
  border-color: #7C5DA8;
  box-shadow: 0 4px 16px rgba(160, 132, 202, 0.15);
}

.user-card {
  border: 1.5px solid #A084CA;
  transition: box-shadow 0.2s, border-color 0.2s;
}

.user-card:hover {
  border-color: #7C5DA8;
  box-shadow: 0 4px 16px rgba(160, 132, 202, 0.15);
}
</style> 