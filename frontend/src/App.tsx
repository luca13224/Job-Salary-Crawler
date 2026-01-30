import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Line, Bar } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { Container, Grid, Card, CardContent, Typography, Box, Button, CssBaseline, ThemeProvider, createTheme, Tabs, Tab } from '@mui/material'
import JobList from './components/JobList'
import Login from './components/Login'
import AdminPanel from './components/AdminPanel'
import AdvancedAnalytics from './components/AdvancedAnalytics'
import AdvancedSearch from './components/AdvancedSearch'
import DataSources from './components/DataSources'
import Top30Jobs from './components/Top30Jobs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend)

const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },
    background: { default: '#f5f5f5' }
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  }
})

function App() {
  const [salaryVals, setSalaryVals] = useState<number[]>([])
  const [byLoc, setByLoc] = useState<any[]>([])
  const [byLevel, setByLevel] = useState<any[]>([])
  const [isAdmin, setIsAdmin] = useState(false)
  const [activeTab, setActiveTab] = useState(0)

  useEffect(() => {
    const base = 'http://127.0.0.1:8081'
    axios.get(base + '/api/analytics/salary_distribution').then(r => setSalaryVals(r.data.values || []))
    axios.get(base + '/api/analytics/by_location').then(r => setByLoc(r.data.data || []))
    axios.get(base + '/api/analytics/by_level').then(r => setByLevel(r.data.data || []))
  }, [])

  const histData = {
    labels: salaryVals.map((_, i) => `Mức ${i + 1}`),
    datasets: [{
      label: 'Lương (triệu VND)',
      data: salaryVals,
      borderColor: 'rgba(75,192,192,1)',
      backgroundColor: 'rgba(75,192,192,0.2)',
      tension: 0.1
    }]
  }

  const locData = {
    labels: byLoc.map(x => x.location),
    datasets: [{
      label: 'Lương TB (triệu VND)',
      data: byLoc.map(x => x.avg_salary),
      backgroundColor: [
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)'
      ]
    }]
  }

  const levelData = {
    labels: byLevel.map(x => x.level || 'N/A'),
    datasets: [{
      label: 'Lương TB (triệu VND)',
      data: byLevel.map(x => x.avg_salary),
      backgroundColor: 'rgba(255, 159, 64, 0.6)'
    }]
  }

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      setIsAdmin(true)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
  }, [])

  const logout = () => {
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    setIsAdmin(false)
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="xl" sx={{ py: 2 }}>
        <Box sx={{ mb: 3 }}>
          <Typography variant="h3" component="h1" sx={{ mb: 1, fontWeight: 'bold' }}>
            📊 Job Market Analytics Platform
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Phân tích chuyên sâu thị trường lao động & mức lương
          </Typography>
        </Box>

        {/* Tab Navigation */}
        <Card sx={{ mb: 2 }}>
          <Tabs 
            value={activeTab} 
            onChange={(_, v) => setActiveTab(v)}
            variant="scrollable"
            scrollButtons="auto"
            sx={{
              borderBottom: '1px solid #eee',
              '& .MuiTab-root': {
                textTransform: 'none',
                fontSize: '15px',
                fontWeight: 500
              }
            }}
          >
            <Tab label="📈 Dashboard Cơ Bản" />
            <Tab label="🔬 Phân Tích Nâng Cao" />
            <Tab label="⭐ Top 30 Cao Lương" />
            <Tab label="📡 Nguồn Dữ liệu" />
            <Tab label="🔍 Tìm Kiếm Nâng Cao" />
            <Tab label="💼 Danh Sách Công Việc" />
            {isAdmin && <Tab label="⚙️ Admin" />}
            <Tab label={isAdmin ? "🚪 Đăng Xuất" : "🔐 Đăng Nhập"} />
          </Tabs>
        </Card>

        {/* Tab Content */}
        <Box>
          {/* Tab 0: Basic Dashboard */}
          {activeTab === 0 && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6} lg={4}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      📈 Phân Bố Lương
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      {salaryVals.length > 0 ? (
                        <Line data={histData} options={{ responsive: true, maintainAspectRatio: false }} />
                      ) : (
                        <Typography color="textSecondary">Đang tải...</Typography>
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6} lg={4}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      🏢 Top Địa Điểm
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      {byLoc.length > 0 ? (
                        <Bar data={locData} options={{ responsive: true, maintainAspectRatio: false }} />
                      ) : (
                        <Typography color="textSecondary">Đang tải...</Typography>
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6} lg={4}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      💼 Theo Cấp Độ
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      {byLevel.length > 0 ? (
                        <Bar data={levelData} options={{ responsive: true, maintainAspectRatio: false }} />
                      ) : (
                        <Typography color="textSecondary">Đang tải...</Typography>
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          )}

          {/* Tab 1: Advanced Analytics */}
          {activeTab === 1 && <AdvancedAnalytics />}

          {/* Tab 2: Top 30 Jobs */}
          {activeTab === 2 && <Top30Jobs />}

          {/* Tab 3: Data Sources */}
          {activeTab === 3 && <DataSources />}

          {/* Tab 4: Advanced Search */}
          {activeTab === 4 && <AdvancedSearch />}

          {/* Tab 5: Job List */}
          {activeTab === 5 && (
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>💼 Danh Sách Công Việc</Typography>
                <JobList />
              </CardContent>
            </Card>
          )}

          {/* Tab 6: Admin */}
          {activeTab === 6 && isAdmin && (
            <Card>
              <CardContent>
                <AdminPanel />
              </CardContent>
            </Card>
          )}

          {/* Tab 7: Auth/Logout */}
          {activeTab === 7 && (
            <Card sx={{ p: 3 }}>
              {!isAdmin ? (
                <Box>
                  <Typography variant="h5" gutterBottom>🔐 Đăng Nhập Admin</Typography>
                  <Login onLogin={() => {
                    setIsAdmin(true)
                    setActiveTab(5)
                  }} />
                </Box>
              ) : (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="h6" gutterBottom>Bạn đã đăng nhập như admin</Typography>
                  <Button 
                    variant="contained" 
                    color="error"
                    onClick={logout}
                    sx={{ mt: 2 }}
                  >
                    Đăng Xuất
                  </Button>
                </Box>
              )}
            </Card>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  )
}

export default App
