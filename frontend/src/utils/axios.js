import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  // 添加跨域配置
  crossDomain: true,
  xhrFields: {
    withCredentials: true
  }
});

// 添加请求拦截器
instance.interceptors.request.use(
  config => {
    // 确保每个请求都带有凭证
    config.withCredentials = true;
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器处理错误
instance.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // 未登录或会话过期，重定向到登录页
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default instance; 