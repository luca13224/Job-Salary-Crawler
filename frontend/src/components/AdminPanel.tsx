import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Box, Card, Typography, Divider, Alert, CircularProgress } from '@mui/material'
import AddJobModal from './AddJobModal'

export default function AdminPanel() {
  const [crawlEnabled, setCrawlEnabled] = useState<number | null>(null)
  const [logs, setLogs] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [addJobOpen, setAddJobOpen] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)

  const fetchSettings = async () => {
    try {
      const r = await axios.get('http://127.0.0.1:8081/api/admin/settings', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
      setCrawlEnabled(r.data.crawl_enabled)
    } catch (e) {
      console.error('Failed to fetch settings', e)
    }
  }

  const toggleCrawl = async (enable: boolean) => {
    setLoading(true)
    try {
      const r = await axios.post('http://127.0.0.1:8081/api/admin/toggle_crawl',
        { enabled: enable ? 1 : 0 },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      )
      setCrawlEnabled(r.data.crawl_enabled)
    } catch (e: any) {
      alert('Lỗi: ' + (e?.response?.data?.detail || e.message))
    } finally {
      setLoading(false)
    }
  }

  const triggerImport = async () => {
    setLoading(true)
    try {
      await axios.post('http://127.0.0.1:8081/api/admin/import', {},
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      )
      alert('Import đã lên lịch')
    } catch (e: any) {
      alert('Lỗi: ' + (e?.response?.data?.detail || e.message))
    } finally {
      setLoading(false)
    }
  }

  const triggerCrawl = async () => {
    setLoading(true)
    try {
      await axios.post('http://127.0.0.1:8081/api/admin/crawl', {},
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      )
      alert('Crawl đã lên lịch')
    } catch (e: any) {
      alert('Lỗi: ' + (e?.response?.data?.detail || e.message))
    } finally {
      setLoading(false)
    }
  }

  const fetchLogs = async () => {
    try {
      const r = await axios.get('http://127.0.0.1:8081/api/admin/logs?lines=100', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
      setLogs(r.data.logs || [])
    } catch (e: any) {
      console.error('Failed to fetch logs', e)
    }
  }

  useEffect(() => { fetchSettings(); fetchLogs() }, [refreshKey])

  useEffect(() => {
    const t = setInterval(fetchLogs, 30_000)
    return () => clearInterval(t)
  }, [])

  return (
    <Box sx={{ mt: 3 }}>
      <AddJobModal 
        open={addJobOpen} 
        onClose={() => setAddJobOpen(false)}
        onSuccess={() => {
          setAddJobOpen(false)
          setRefreshKey(k => k + 1)
        }}
      />

      <Card sx={{ p: 3 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>Bảng điều khiển Admin</Typography>
        
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 3, flexWrap: 'wrap' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography><strong>Crawl:</strong></Typography>
            <Typography sx={{ color: crawlEnabled ? 'green' : 'red' }}>
              {crawlEnabled === null ? 'Đang tải...' : (crawlEnabled ? '✓ Bật' : '✗ Tắt')}
            </Typography>
          </Box>
          
          <Button 
            variant="contained" 
            size="small"
            onClick={() => toggleCrawl(true)}
            disabled={loading || crawlEnabled === 1}
          >
            Bật Crawl
          </Button>
          
          <Button 
            variant="outlined" 
            size="small"
            onClick={() => toggleCrawl(false)}
            disabled={loading || crawlEnabled === 0}
          >
            Tắt Crawl
          </Button>
          
          <Button 
            variant="contained" 
            size="small"
            onClick={triggerImport}
            disabled={loading}
          >
            Nhập Dữ liệu
          </Button>
          
          <Button 
            variant="contained" 
            size="small"
            onClick={triggerCrawl}
            disabled={loading}
          >
            Chạy Crawl
          </Button>

          <Button 
            variant="contained" 
            color="success"
            size="small"
            onClick={() => setAddJobOpen(true)}
          >
            + Thêm Job
          </Button>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Typography variant="h6" sx={{ mb: 2 }}>Logs Admin (100 dòng gần nhất)</Typography>
        <Box sx={{
          maxHeight: 300,
          overflow: 'auto',
          background: '#1a1a1a',
          color: '#00ff00',
          padding: 2,
          borderRadius: 1,
          fontFamily: 'monospace',
          fontSize: '12px'
        }}>
          {logs.length === 0 ? (
            <Typography sx={{ color: '#666' }}>Không có logs</Typography>
          ) : (
            logs.map((l, i) => (
              <Box key={i}><small>{l}</small></Box>
            ))
          )}
        </Box>
      </Card>
    </Box>
  )
}
