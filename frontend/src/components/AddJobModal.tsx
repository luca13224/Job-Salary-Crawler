import React, { useState } from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  Typography
} from '@mui/material'
import axios from 'axios'

interface AddJobModalProps {
  open: boolean
  onClose: () => void
  onSuccess?: () => void
}

export default function AddJobModal({ open, onClose, onSuccess }: AddJobModalProps) {
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    salary_raw: '',
    location: '',
    level: ''
  })
  const [avgSalary, setAvgSalary] = useState<number | null>(null)
  const [parsing, setParsing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleParseSalary = async () => {
    if (!formData.salary_raw.trim()) {
      setError('Nhập chuỗi lương trước')
      return
    }
    setParsing(true)
    setError(null)
    try {
      const r = await axios.post('http://127.0.0.1:8081/api/parse_salary', {
        salary_raw: formData.salary_raw
      })
      if (r.data.error) {
        setError(r.data.error)
      } else {
        setAvgSalary(r.data.avg_salary_mil_vnd)
      }
    } catch (e: any) {
      setError(`Parse lỗi: ${e.message}`)
    } finally {
      setParsing(false)
    }
  }

  const handleSave = async () => {
    if (!formData.title || !formData.company) {
      setError('Vui lòng điền chức vụ và công ty')
      return
    }
    setSaving(true)
    setError(null)
    try {
      await axios.post('http://127.0.0.1:8081/api/admin/jobs/create', {
        ...formData,
        avg_salary_mil_vnd: avgSalary
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
      setFormData({ title: '', company: '', salary_raw: '', location: '', level: '' })
      setAvgSalary(null)
      onSuccess?.()
      onClose()
    } catch (e: any) {
      setError(`Lưu lỗi: ${e.response?.data?.detail || e.message}`)
    } finally {
      setSaving(false)
    }
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Thêm công việc mới</DialogTitle>
      <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
        {error && <Alert severity="error">{error}</Alert>}
        
        <TextField
          label="Chức vụ *"
          value={formData.title}
          onChange={e => setFormData({...formData, title: e.target.value})}
          fullWidth
          size="small"
        />
        
        <TextField
          label="Công ty *"
          value={formData.company}
          onChange={e => setFormData({...formData, company: e.target.value})}
          fullWidth
          size="small"
        />
        
        <TextField
          label="Cấp độ"
          value={formData.level}
          onChange={e => setFormData({...formData, level: e.target.value})}
          fullWidth
          size="small"
        />
        
        <TextField
          label="Địa điểm"
          value={formData.location}
          onChange={e => setFormData({...formData, location: e.target.value})}
          fullWidth
          size="small"
        />
        
        <Box>
          <Typography variant="subtitle2" sx={{ mb: 1 }}>Lương (chuỗi thô)</Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              label="VD: 15 - 25 triệu"
              value={formData.salary_raw}
              onChange={e => setFormData({...formData, salary_raw: e.target.value})}
              fullWidth
              size="small"
            />
            <Button 
              variant="outlined" 
              onClick={handleParseSalary}
              disabled={parsing}
              sx={{ whiteSpace: 'nowrap' }}
            >
              {parsing ? <CircularProgress size={20} /> : 'Parse'}
            </Button>
          </Box>
          
          {avgSalary !== null && (
            <Typography variant="body2" sx={{ mt: 1, color: 'green' }}>
              ✓ Mức lương: {avgSalary.toLocaleString()} triệu VND
            </Typography>
          )}
        </Box>
      </DialogContent>
      
      <DialogActions>
        <Button onClick={onClose}>Hủy</Button>
        <Button 
          onClick={handleSave}
          variant="contained"
          disabled={saving || !formData.title || !formData.company}
        >
          {saving ? <CircularProgress size={20} /> : 'Lưu'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}
