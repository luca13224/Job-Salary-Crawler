import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Box, Card, Typography, Grid, CircularProgress, Alert } from '@mui/material'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#6C5CE7', '#A29BFE', '#74B9FF']

export default function AdvancedAnalytics() {
  const [salaryStats, setSalaryStats] = useState<any>(null)
  const [salaryByLevel, setSalaryByLevel] = useState<any[]>([])
  const [salaryByLocation, setSalaryByLocation] = useState<any[]>([])
  const [topSkills, setTopSkills] = useState<any[]>([])
  const [companies, setCompanies] = useState<any[]>([])
  const [topTitles, setTopTitles] = useState<any[]>([])
  const [distribution, setDistribution] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const base = 'http://127.0.0.1:8081'

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true)
      setError(null)
      try {
        const [stats, level, location, skills, companies, titles, dist] = await Promise.all([
          axios.get(`${base}/api/analytics/salary-stats`),
          axios.get(`${base}/api/analytics/salary-by-level`),
          axios.get(`${base}/api/analytics/salary-by-location?limit=10`),
          axios.get(`${base}/api/analytics/top-skills?limit=15`),
          axios.get(`${base}/api/analytics/company-analysis?limit=12`),
          axios.get(`${base}/api/analytics/title-salary-insights?limit=10`),
          axios.get(`${base}/api/analytics/salary-distribution?bins=12`)
        ])
        
        setSalaryStats(stats.data)
        setSalaryByLevel(level.data)
        setSalaryByLocation(location.data)
        setTopSkills(skills.data)
        setCompanies(companies.data)
        setTopTitles(titles.data)
        setDistribution(dist.data)
      } catch (e: any) {
        setError(`Lỗi: ${e?.response?.data?.detail || e.message}`)
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    fetchAnalytics()
  }, [])

  if (loading) return <Box sx={{ p: 3, display: 'flex', justifyContent: 'center' }}><CircularProgress /></Box>
  if (error) return <Alert severity="error" sx={{ m: 2 }}>{error}</Alert>

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 'bold' }}>📊 Phân tích thị trường lao động nâng cao</Typography>
      
      {/* KPI Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ p: 2, textAlign: 'center', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
            <Typography variant="h6">Tổng công việc</Typography>
            <Typography variant="h3">{salaryStats?.count || 0}</Typography>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ p: 2, textAlign: 'center', background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
            <Typography variant="h6">Lương trung bình</Typography>
            <Typography variant="h3">{salaryStats?.avg?.toFixed(1) || 0} triệu</Typography>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ p: 2, textAlign: 'center', background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
            <Typography variant="h6">Lương cao nhất</Typography>
            <Typography variant="h3">{salaryStats?.max || 0} triệu</Typography>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ p: 2, textAlign: 'center', background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)', color: 'white' }}>
            <Typography variant="h6">Lương thấp nhất</Typography>
            <Typography variant="h3">{salaryStats?.min || 0} triệu</Typography>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Row 1 */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>💰 Lương theo Cấp độ</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={salaryByLevel}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="level" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="avg_salary" fill="#8884d8" name="Lương trung bình" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>📍 Top 10 địa điểm cao lương</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={salaryByLocation} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="location" type="category" width={100} />
                <Tooltip />
                <Bar dataKey="avg_salary" fill="#82ca9d" name="Lương TB" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Row 2 */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>🔧 Top 15 Skills theo nhu cầu</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topSkills}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="skill" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="frequency" fill="#ffc658" name="Tần suất" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>💼 Top công ty tuyển dụng</Typography>
            <Box sx={{ maxHeight: 300, overflowY: 'auto' }}>
              {companies.map((c, i) => (
                <Box key={i} sx={{ p: 1.5, borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{i + 1}. {c.company}</Typography>
                    <Typography variant="caption" sx={{ color: '#666' }}>
                      {c.job_count} vị trí • Lương TB: {c.avg_salary} triệu
                    </Typography>
                  </Box>
                  <Box sx={{ background: '#e8f5e9', px: 2, py: 1, borderRadius: 1 }}>
                    <Typography variant="body2" sx={{ color: '#2e7d32', fontWeight: 'bold' }}>{c.job_count}</Typography>
                  </Box>
                </Box>
              ))}
            </Box>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Row 3 */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>📈 Phân bố lương</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={distribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="bin" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#ff7c7c" name="Số người" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>⭐ Top vị trí cao lương</Typography>
            <Box sx={{ maxHeight: 300, overflowY: 'auto' }}>
              {topTitles.map((t, i) => (
                <Box key={i} sx={{ p: 1.5, borderBottom: '1px solid #eee' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{i + 1}. {t.title}</Typography>
                      <Typography variant="caption" sx={{ color: '#666' }}>
                        {t.count} vị trí • Lương TB
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ background: '#fff3e0', px: 2, py: 1, borderRadius: 1, color: '#e65100', fontWeight: 'bold' }}>
                      {t.avg_salary} triệu
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Box>
          </Card>
        </Grid>
      </Grid>

      {/* Skills Salary Analysis */}
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>🎯 Phân tích kỹ năng - Lương cao nhất</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topSkills.sort((a, b) => b.avg_salary - a.avg_salary)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="skill" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="avg_salary" fill="#a4de6c" name="Lương TB (triệu)" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}
