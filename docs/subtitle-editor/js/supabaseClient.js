import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

// Supabase配置 - 这些值需要在Supabase控制台获取
const SUPABASE_URL = 'https://your-project.supabase.co'  // 替换为您的Supabase URL
const SUPABASE_ANON_KEY = 'your-anon-key'  // 替换为您的匿名密钥

// 创建Supabase客户端
export const sb = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// 获取当前会话
export async function getSession() {
    return (await sb.auth.getSession()).data.session
}

// 获取当前用户
export async function getCurrentUser() {
    const { data: { user } } = await sb.auth.getUser()
    return user
}

// 检查是否已登录
export async function isAuthenticated() {
    const session = await getSession()
    return !!session
}

// 登录
export async function signIn(email, password) {
    const { data, error } = await sb.auth.signInWithPassword({
        email,
        password
    })
    return { data, error }
}

// 注册
export async function signUp(email, password) {
    const { data, error } = await sb.auth.signUp({
        email,
        password
    })
    return { data, error }
}

// 登出
export async function signOut() {
    const { error } = await sb.auth.signOut()
    return { error }
}

// 监听认证状态变化
export function onAuthStateChange(callback) {
    return sb.auth.onAuthStateChange(callback)
}
