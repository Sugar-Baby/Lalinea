<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" lg="6" class="mx-auto">
        <h1 class="mb-6">个人信息</h1>
        <v-card>
          <v-card-text>
            <v-form>
              <v-text-field label="学号" v-model="user.student_id" readonly></v-text-field>
              <v-text-field label="姓名" v-model="user.name" :readonly="!infoEditMode"></v-text-field>
              <v-text-field label="邮箱" v-model="user.email" :readonly="!infoEditMode"></v-text-field>
              <v-text-field label="联系方式" v-model="user.contact" :readonly="!infoEditMode"></v-text-field>
            </v-form>
            <div class="d-flex align-center mt-4 mb-2">
              <span class="font-weight-bold">我的标签</span>
              <v-spacer />
              <v-btn size="small" @click="toggleTagEditMode" color="primary" variant="tonal">
                {{ tagEditMode ? '完成标签编辑' : '编辑标签' }}
              </v-btn>
            </div>
            <div class="mb-2" v-if="tagEditMode">
              <v-text-field
                v-model="tagInput"
                label="输入标签后回车添加"
                @keyup.enter="addTag"
                clearable
                hide-details
                :disabled="!tagEditMode"
              ></v-text-field>
            </div>
            <div class="tag-box mt-2 mb-4">
              <v-chip
                v-for="tag in user.hobbies"
                :key="tag"
                class="ma-1"
                color="primary"
                variant="tonal"
                closable
                @click:close="removeTag(tag)"
                :disabled="!tagEditMode"
              >
                {{ tag }}
              </v-chip>
              <span v-if="!user.hobbies.length" class="text-grey">暂无标签</span>
            </div>
            <div class="text-caption mb-2">点击标签右侧的"×"可删除，标签编辑模式下可添加/删除标签</div>
            <v-btn color="primary" class="mr-2" @click="toggleInfoEditMode">{{ infoEditMode ? '完成信息编辑' : '编辑信息' }}</v-btn>
            <v-btn color="error" variant="tonal" @click="logout">退出登录</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from '@/utils/axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const user = reactive({ student_id: '', name: '', email: '', contact: '', hobbies: [] });
const infoEditMode = ref(false);
const tagEditMode = ref(false);
const tagInput = ref('');

const fetchProfile = async () => {
  const res = await axios.get('/api/user/me');
  Object.assign(user, res.data);
};

const toggleInfoEditMode = async () => {
  if (infoEditMode.value) {
    // 完成编辑，自动保存
    await axios.put('/api/user/me', {
      name: user.name,
      email: user.email,
      contact: user.contact
    });
    infoEditMode.value = false;
    alert('保存成功');
  } else {
    infoEditMode.value = true;
  }
};

const toggleTagEditMode = async () => {
  if (tagEditMode.value) {
    // 完成标签编辑，保存到服务器
    await axios.put('/api/user/me/hobbies', {
      hobbies: user.hobbies
    });
    tagEditMode.value = false;
    alert('标签已保存');
  } else {
    tagEditMode.value = true;
  }
  tagInput.value = '';
};

const addTag = async () => {
  const val = tagInput.value.trim();
  if (!val || user.hobbies.includes(val)) {
    tagInput.value = '';
    return;
  }
  // 先尝试添加到标签库
  await axios.post('/api/hobbies', { name: val });
  user.hobbies.push(val);
  tagInput.value = '';
};

const removeTag = (tag) => {
  user.hobbies = user.hobbies.filter(t => t !== tag);
};

const saveProfile = async () => {
  await axios.put('/api/user/me', {
    name: user.name,
    email: user.email,
    contact: user.contact
  });
  await axios.put('/api/user/me/hobbies', {
    hobbies: user.hobbies
  });
  infoEditMode.value = false;
  tagEditMode.value = false;
  alert('保存成功');
};

const logout = () => {
  // 清除所有本地存储
  localStorage.clear();
  // 触发登录状态更新事件
  window.dispatchEvent(new Event('loginStateChanged'));
  // 确保重定向到首页
  router.replace('/');
  // 监听路由变化，在到达首页后刷新
  const unwatch = router.afterEach((to) => {
    if (to.path === '/') {
      window.location.reload();
      unwatch(); // 移除监听器
    }
  });
};

onMounted(fetchProfile);
</script>

<style scoped>
.tag-box {
  min-height: 48px;
  background: rgba(160, 132, 202, 0.06);
  border-radius: 8px;
  padding: 8px 12px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}
</style> 