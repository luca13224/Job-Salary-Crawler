import React, { useState, useCallback, useRef } from 'react'
import axios from 'axios'
import { Box, Card, TextField, Button, Grid, Slider, Typography, Chip, CircularProgress, Autocomplete } from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'

export default function AdvancedSearch() {
  const [jobs, setJobs] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [total, setTotal] = useState(0)
  const [pagination, setPagination] = useState({ pageSize: 20, page: 0 })
  const debounceTimer = useRef<any>(null)
  
  // Filter states
  const [title, setTitle] = useState('')
  const [titleSuggestions, setTitleSuggestions] = useState<string[]>([])
  
  const [location, setLocation] = useState('')
  const [locationSuggestions, setLocationSuggestions] = useState<string[]>([])
  
  const [level, setLevel] = useState('')
  const [levelSuggestions, setLevelSuggestions] = useState<string[]>([])
  
  const [skills, setSkills] = useState('')
  const [skillSuggestions, setSkillSuggestions] = useState<string[]>([])
  
  const [company, setCompany] = useState('')
  const [companySuggestions, setCompanySuggestions] = useState<string[]>([])
  
  const [salary, setSalary] = useState<[number, number]>([0, 150])

  const base = 'http://127.0.0.1:8081'

  // Debounced fetch suggestions
  const fetchWithDebounce = (callback: () => Promise<void>) => {
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current)
    }
    debounceTimer.current = setTimeout(callback, 300)
  }

  const fetchTitleSuggestions = async (query: string) => {
    if (!query || query.length < 1) {
      setTitleSuggestions([])
      return
    }
    try {
      const r = await axios.get(`${base}/api/suggestions/titles?q=${query}&limit=15`)
      setTitleSuggestions(r.data.suggestions || [])
    } catch (e) {
      console.error(e)
    }
  }

  const fetchCompanySuggestions = async (query: string) => {
    if (!query || query.length < 1) {
      setCompanySuggestions([])
      return
    }
    try {
      const r = await axios.get(`${base}/api/suggestions/companies?q=${query}&limit=15`)
      setCompanySuggestions(r.data.suggestions || [])
    } catch (e) {
      console.error(e)
    }
  }

  const fetchLocationSuggestions = async (query: string) => {
    if (!query || query.length < 1) {
      setLocationSuggestions([])
      return
    }
    try {
      const r = await axios.get(`${base}/api/suggestions/locations?q=${query}&limit=15`)
      setLocationSuggestions(r.data.suggestions || [])
    } catch (e) {
      console.error(e)
    }
  }

  const fetchLevelSuggestions = async (query: string) => {
    if (!query || query.length < 1) {
      setLevelSuggestions([])
      return
    }
    try {
      const r = await axios.get(`${base}/api/suggestions/levels?q=${query}&limit=15`)
      setLevelSuggestions(r.data.suggestions || [])
    } catch (e) {
      console.error(e)
    }
  }

  const fetchSkillSuggestions = async (query: string) => {
    if (!query || query.length < 1) {
      setSkillSuggestions([])
      return
    }
    try {
      const r = await axios.get(`${base}/api/suggestions/skills?q=${query}&limit=15`)
      setSkillSuggestions(r.data.suggestions || [])
    } catch (e) {
      console.error(e)
    }
  }

  const handleSearch = useCallback(async () => {
    setLoading(true)
    try {
      const params: any = {
        page: pagination.page + 1,
        per_page: pagination.pageSize
      }
      if (title) params.title = title
      if (location) params.location = location
      if (level) params.level = level
      if (salary[0] > 0) params.min_salary = salary[0]
      if (salary[1] < 150) params.max_salary = salary[1]
      
      const r = await axios.get(`${base}/api/jobs`, { params })
      
      // Filter by company and skills on frontend
      let filtered = r.data.items
      if (company) filtered = filtered.filter((j: any) => j.company?.toLowerCase().includes(company.toLowerCase()))
      if (skills) {
        const skillsArray = skills.split(',').map(s => s.trim().toLowerCase())
        filtered = filtered.filter((j: any) => 
          j.skills && skillsArray.some(s => j.skills.toLowerCase().includes(s))
        )
      }

      setJobs(filtered.map((item: any, idx: number) => ({ ...item, id: item.id || idx })))
      setTotal(r.data.total)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }, [pagination, title, location, level, salary, company, skills])

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'title', headerName: 'Chức vụ', width: 250, flex: 1 },
    { field: 'company', headerName: 'Công ty', width: 180 },
    { field: 'level', headerName: 'Level', width: 100 },
    { field: 'avg_salary_mil_vnd', headerName: 'Lương (triệu)', width: 120, type: 'number' },
    { field: 'location', headerName: 'Địa điểm', width: 140 },
    { field: 'skills', headerName: 'Kỹ năng', width: 250, renderCell: (params) => (
      <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
        {params.value?.split(',').slice(0, 3).map((skill: string, i: number) => (
          <Chip key={i} label={skill.trim()} size="small" variant="outlined" />
        ))}
        {params.value?.split(',').length > 3 && <Chip label="+..." size="small" />}
      </Box>
    )}
  ]

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 'bold' }}>🔍 Tìm kiếm nâng cao</Typography>
      
      <Card sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={4}>
            <Autocomplete
              freeSolo
              options={titleSuggestions}
              value={title}
              onChange={(_, newValue) => setTitle(newValue || '')}
              onInputChange={(_, newValue) => {
                setTitle(newValue)
                fetchWithDebounce(() => fetchTitleSuggestions(newValue))
              }}
              noOptionsText="Không tìm thấy"
              loadingText="Đang tải..."
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Chức vụ"
                  placeholder="Lập trình viên, Designer..."
                  size="small"
                />
              )}
            />
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <Autocomplete
              freeSolo
              options={companySuggestions}
              value={company}
              onChange={(_, newValue) => setCompany(newValue || '')}
              onInputChange={(_, newValue) => {
                setCompany(newValue)
                fetchWithDebounce(() => fetchCompanySuggestions(newValue))
              }}
              noOptionsText="Không tìm thấy"
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Công ty"
                  placeholder="Tên công ty..."
                  size="small"
                />
              )}
            />
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <Autocomplete
              freeSolo
              options={locationSuggestions}
              value={location}
              onChange={(_, newValue) => setLocation(newValue || '')}
              onInputChange={(_, newValue) => {
                setLocation(newValue)
                fetchWithDebounce(() => fetchLocationSuggestions(newValue))
              }}
              noOptionsText="Không tìm thấy"
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Địa điểm"
                  placeholder="TP.HCM, Hà Nội..."
                  size="small"
                />
              )}
            />
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <Autocomplete
              freeSolo
              options={levelSuggestions}
              value={level}
              onChange={(_, newValue) => setLevel(newValue || '')}
              onInputChange={(_, newValue) => {
                setLevel(newValue)
                fetchWithDebounce(() => fetchLevelSuggestions(newValue))
              }}
              noOptionsText="Không tìm thấy"
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Cấp độ"
                  placeholder="Intern, Junior, Senior..."
                  size="small"
                />
              )}
            />
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <Autocomplete
              freeSolo
              options={skillSuggestions}
              value={skills}
              onChange={(_, newValue) => setSkills(newValue || '')}
              onInputChange={(_, newValue) => {
                setSkills(newValue)
                fetchWithDebounce(() => fetchSkillSuggestions(newValue))
              }}
              noOptionsText="Không tìm thấy"
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Kỹ năng"
                  placeholder="React, Node.js..."
                  size="small"
                />
              )}
            />
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Button
              fullWidth
              variant="contained"
              onClick={handleSearch}
              disabled={loading}
              sx={{ height: '40px' }}
            >
              {loading ? <CircularProgress size={24} /> : '🔍 Tìm kiếm'}
            </Button>
          </Grid>
        </Grid>

        {/* Salary Range Slider */}
        <Box>
          <Typography variant="subtitle2" sx={{ mb: 2 }}>💰 Mức lương: {salary[0]} - {salary[1]} triệu VND</Typography>
          <Slider
            value={salary}
            onChange={(_, newValue) => setSalary(newValue as [number, number])}
            valueLabelDisplay="auto"
            min={0}
            max={150}
            step={5}
            marks={[
              { value: 0, label: '0' },
              { value: 75, label: '75' },
              { value: 150, label: '150+' }
            ]}
            sx={{ mb: 2 }}
          />
        </Box>

        {/* Applied Filters */}
        {(title || company || location || level || skills || salary[0] > 0 || salary[1] < 150) && (
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', alignItems: 'center' }}>
            <Typography variant="caption" sx={{ color: '#666' }}>Bộ lọc đang áp dụng:</Typography>
            {title && <Chip label={`Chức vụ: ${title}`} size="small" onDelete={() => setTitle('')} />}
            {company && <Chip label={`Công ty: ${company}`} size="small" onDelete={() => setCompany('')} />}
            {location && <Chip label={`Địa điểm: ${location}`} size="small" onDelete={() => setLocation('')} />}
            {level && <Chip label={`Level: ${level}`} size="small" onDelete={() => setLevel('')} />}
            {skills && <Chip label={`Skills: ${skills}`} size="small" onDelete={() => setSkills('')} />}
            {(salary[0] > 0 || salary[1] < 150) && <Chip label={`Lương: ${salary[0]}-${salary[1]}M`} size="small" onDelete={() => setSalary([0, 150])} />}
          </Box>
        )}
      </Card>

      {/* Results Summary */}
      {jobs.length > 0 && (
        <Card sx={{ p: 2, mb: 2, background: '#e3f2fd' }}>
          <Typography variant="body2">
            ✓ Tìm thấy <strong>{jobs.length}</strong> kết quả (Tổng: <strong>{total}</strong> công việc khớp)
          </Typography>
        </Card>
      )}

      {/* Results */}
      <Card>
        <Box sx={{ height: 600, width: '100%' }}>
          <DataGrid
            rows={jobs}
            columns={columns}
            paginationModel={pagination}
            onPaginationModelChange={setPagination}
            pageSizeOptions={[10, 20, 50]}
            rowCount={total}
            loading={loading}
            paginationMode="server"
            disableRowSelectionOnClick
            sx={{
              '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f5f5f5' },
              '& .MuiDataGrid-row:hover': { backgroundColor: '#f9f9f9' }
            }}
          />
        </Box>
      </Card>
    </Box>
  )
}
