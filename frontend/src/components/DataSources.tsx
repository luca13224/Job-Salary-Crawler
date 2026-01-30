import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Box, Card, Typography, Grid, CircularProgress, Alert, Chip, LinearProgress, Paper } from '@mui/material'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts'

const COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#6C5CE7', '#A29BFE', '#74B9FF']

export default function DataSources() {
  const [overview, setOverview] = useState<any>(null)
  const [sources, setSources] = useState<any[]>([])
  const [trending, setTrending] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const base = 'http://127.0.0.1:8081'

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError(null)
      try {
        const [overviewRes, sourcesRes, trendingRes] = await Promise.all([
          axios.get(`${base}/api/analytics/market-overview`),
          axios.get(`${base}/api/analytics/data-sources`),
          axios.get(`${base}/api/analytics/trending-jobs?limit=15`)
        ])
        
        setOverview(overviewRes.data)
        setSources(sourcesRes.data)
        setTrending(trendingRes.data)
      } catch (e: any) {
        setError(`Lỗi: ${e?.response?.data?.detail || e.message}`)
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <Box sx={{ p: 3, display: 'flex', justifyContent: 'center' }}><CircularProgress /></Box>
  if (error) return <Alert severity="error" sx={{ m: 2 }}>{error}</Alert>

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 'bold' }}>📡 Nguồn Dữ liệu & Market Overview</Typography>
      
      {/* Market Overview Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ p: 2, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>Tổng Jobs</Typography>
            <Typography variant="h3">{overview?.total_jobs || 0}</Typography>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ p: 2, background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>Có Lương</Typography>
            <Typography variant="h3">{overview?.jobs_with_salary || 0}</Typography>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ p: 2, background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>Hoàn Chỉnh</Typography>
            <Typography variant="h3">{overview?.data_completeness || 0}%</Typography>
            <LinearProgress variant="determinate" value={overview?.data_completeness || 0} sx={{ mt: 1 }} />
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ p: 2, background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)', color: 'white' }}>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>Số Sources</Typography>
            <Typography variant="h3">{overview?.sources?.length || 0}</Typography>
          </Card>
        </Grid>
      </Grid>

      {/* Data Sources */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>📊 Jobs theo Nguồn</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie dataKey="count" data={sources} cx="50%" cy="50%" labelLine={false} label={({ name, value }) => `${name}: ${value}`}>
                  {sources.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>🌐 Chi Tiết Nguồn Dữ liệu</Typography>
            <Box sx={{ maxHeight: 350, overflowY: 'auto' }}>
              {sources.map((source, i) => (
                <Paper key={i} sx={{ p: 2, mb: 1, background: 'linear-gradient(90deg, rgba(100,200,200,0.1) 0%, transparent 100%)' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      {source.source || 'Unknown'} ({source.count} jobs)
                    </Typography>
                    <Chip label={`${Math.round(source.count / (overview?.total_jobs || 1) * 100)}%`} color="primary" size="small" />
                  </Box>
                  <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 1, fontSize: '12px', color: '#666' }}>
                    <Box>Lương TB: <strong>{source.avg_salary?.toFixed(1) || 'N/A'} triệu</strong></Box>
                    <Box>Lần cuối: <strong>{source.last_crawled?.split('T')[0] || 'N/A'}</strong></Box>
                  </Box>
                </Paper>
              ))}
            </Box>
          </Card>
        </Grid>
      </Grid>

      {/* Top Locations */}
      {overview?.top_locations && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12}>
            <Card sx={{ p: 2 }}>
              <Typography variant="h6" sx={{ mb: 2 }}>📍 Top 5 Thành Phố Tuyển Dụng</Typography>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={overview.top_locations}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="location" angle={-30} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#82ca9d" name="Số Jobs" />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Trending/Recent Jobs */}
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>🔥 Top 15 Jobs Mới Nhất (30 ngày)</Typography>
            <Box sx={{ maxHeight: 500, overflowY: 'auto' }}>
              {trending.map((job, i) => (
                <Paper key={i} sx={{ p: 2, mb: 1.5, background: '#f9f9f9', borderLeft: '4px solid #4facfe' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 1 }}>
                    <Box>
                      <Typography variant="body2" sx={{ fontWeight: 'bold', color: '#1976d2' }}>
                        {job.title}
                      </Typography>
                      <Typography variant="caption" sx={{ color: '#666' }}>
                        {job.company} • {job.source}
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ background: '#e3f2fd', px: 1.5, py: 0.5, borderRadius: 1, fontWeight: 'bold', color: '#1976d2', whiteSpace: 'nowrap' }}>
                      {job.salary?.toFixed(1) || 'TBD'} M
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', alignItems: 'center' }}>
                    <Chip label={`📅 ${job.crawled_at?.split('T')[0]}`} size="small" variant="outlined" />
                    {job.url && (
                      <a href={job.url} target="_blank" rel="noopener noreferrer" style={{ fontSize: '12px', color: '#4facfe', textDecoration: 'none' }}>
                        🔗 Xem chi tiết
                      </a>
                    )}
                  </Box>
                </Paper>
              ))}
            </Box>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}
