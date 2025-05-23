<template>
  <div class="home">
    <div class="hero">
      <h1 class="title">Lalinea</h1>
      <p class="subtitle">连接校园，发现志同道合的朋友</p>
    </div>

    <div class="features">
      <div class="feature-card">
        <h2>创建你的个人档案</h2>
        <p>使用学号和姓名创建账号，添加你的联系方式，让更多人认识你</p>
      </div>

      <div class="feature-card">
        <h2>标记你的兴趣</h2>
        <p>选择或创建标签，展示你的特长和兴趣领域</p>
      </div>

      <div class="feature-card">
        <h2>发现新朋友</h2>
        <p>通过标签或名字搜索，找到志同道合的伙伴</p>
      </div>

      <div class="feature-card">
        <h2>社交距离</h2>
        <p>系统会计算你与其他人或兴趣圈子的社交距离，帮助你更好地了解彼此</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// 组件逻辑
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
  /* background-color: #fff; 移除固定背景色 */
}

.hero {
  text-align: center;
  margin-bottom: 4rem;
}

.title {
  font-size: 3.5rem;
  color: #7C5DA8;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.5rem;
  color: #000;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  /* background: #fff; 移除固定背景色 */
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h2 {
  color: #7C5DA8;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #333;
  line-height: 1.6;
}

/* 已移除theme.css依赖，全部使用静态色值或Vuetify主题色 */
</style>
