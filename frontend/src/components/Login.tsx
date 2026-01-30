import React, { useState } from 'react'
import axios from 'axios'

export default function Login({ onLogin }: { onLogin: () => void }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const submit = async () => {
    try {
      const data = new URLSearchParams()
      data.append('username', username)
      data.append('password', password)
      const r = await axios.post('http://127.0.0.1:8081/api/auth/login', data)
      const token = r.data.access_token
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      onLogin()
    } catch (e:any) {
      setError(e?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div style={{padding:12, border:'1px solid #eee', borderRadius:6, marginTop:12}}>
      <h4>Admin login</h4>
      <div style={{display:'flex', gap:8}}>
        <input placeholder="username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button onClick={submit}>Login</button>
      </div>
      {error && <div style={{color:'red', marginTop:8}}>{error}</div>}
    </div>
  )
}
