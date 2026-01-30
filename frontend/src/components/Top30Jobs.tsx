import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Box, Card, Typography, CircularProgress, Alert, Chip, Paper } from '@mui/material'

export default function Top30Jobs() {
  const [jobs, setJobs] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const base = 'http://127.0.0.1:8081'

  useEffect(() => {
    const fetchJobs = async () => {
      setLoading(true)
      setError(null)
      try {
        const r = await axios.get(`${base}/api/analytics/top-30-jobs`)
        setJobs(r.data || [])
      } catch (e: any) {
        setError(`Lỗi: ${e?.response?.data?.detail || e.message}`)
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    fetchJobs()
  }, [])

  if (loading) return <Box sx={{ p: 3, display: 'flex', justifyContent: 'center' }}><CircularProgress /></Box>
  if (error) return <Alert severity="error" sx={{ m: 2 }}>{error}</Alert>

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 'bold' }}>⭐ Top 30 Công Việc Cao Lương</Typography>
      
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 2 }}>
        {jobs.map((job, i) => (
          <Paper key={i} sx={{ p: 2.5, display: 'flex', flexDirection: 'column', gap: 1.5, hover: { boxShadow: 3 }, transition: 'all 0.3s' }}>
            {/* Rank & Salary */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                <Box sx={{
                  background: i < 10 ? '#FFD700' : i < 20 ? '#C0C0C0' : '#CD7F32',
                  color: 'white',
                  width: 32,
                  height: 32,
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 'bold',
                  fontSize: '14px'
                }}>
                  {i + 1}
                </Box>
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#1976d2' }}>
                    {job.title}
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#666' }}>
                    {job.company}
                  </Typography>
                </Box>
              </Box>
              <Box sx={{ textAlign: 'right' }}>
                <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#2e7d32' }}>
                  {job.salary} M
                </Typography>
                <Typography variant="caption" sx={{ color: '#999' }}>triệu VND</Typography>
              </Box>
            </Box>

            {/* Details */}
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {job.level && (
                <Chip
                  label={job.level}
                  size="small"
                  variant="outlined"
                  color="primary"
                />
              )}
              {job.location && (
                <Chip
                  label={`📍 ${job.location}`}
                  size="small"
                  variant="outlined"
                />
              )}
              <Chip
                label={`${job.source || 'Unknown'}`}
                size="small"
                variant="filled"
                sx={{ background: '#e3f2fd', color: '#1976d2' }}
              />
            </Box>

            {/* Skills */}
            {job.skills && (
              <Box>
                <Typography variant="caption" sx={{ color: '#666', display: 'block', mb: 0.5 }}>
                  Kỹ năng:
                </Typography>
                <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                  {job.skills.split(',').slice(0, 5).map((skill: string, i: number) => (
                    <Chip key={i} label={skill.trim()} size="small" />
                  ))}
                  {job.skills.split(',').length > 5 && (
                    <Chip label={`+${job.skills.split(',').length - 5}`} size="small" />
                  )}
                </Box>
              </Box>
            )}

            {/* Date & Link */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', pt: 1, borderTop: '1px solid #eee' }}>
              <Typography variant="caption" sx={{ color: '#999' }}>
                📅 {job.crawled_at?.split('T')[0] || 'N/A'}
              </Typography>
              {job.url && (
                <a href={job.url} target="_blank" rel="noopener noreferrer" style={{
                  fontSize: '12px',
                  color: '#1976d2',
                  textDecoration: 'none',
                  fontWeight: 'bold'
                }}>
                  🔗 Xem chi tiết →
                </a>
              )}
            </Box>
          </Paper>
        ))}
      </Box>

      {jobs.length === 0 && (
        <Alert severity="info">Không có dữ liệu về lương</Alert>
      )}
    </Box>
  )
}
