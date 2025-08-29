import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

// Supabase配置 - 已配置
const SUPABASE_URL = 'https://smzmgemipnxcimsxhewi.supabase.co'
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNtem1nZW1pcG54Y2ltc3hoZXdpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY0NzUyMjIsImV4cCI6MjA3MjA1MTIyMn0.b2H8EFSlUIGL7DwcNWjAG1Ox0FS6Hil8zagHp4rBfUM'

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
