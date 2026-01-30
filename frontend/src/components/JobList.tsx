import React, { useEffect, useState, useCallback } from 'react'
import axios from 'axios'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import { Button, Box, Alert, CircularProgress, Autocomplete, TextField } from '@mui/material'
import * as XLSX from 'xlsx'

export default function JobList() {
  const [rows, setRows] = useState<any[]>([])
  const [paginationModel, setPaginationModel] = useState({ pageSize: 20, page: 0 })
  const [rowCount, setRowCount] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sortModel, setSortModel] = useState([{ field: 'avg_salary_mil_vnd', sort: 'desc' }])
  const [filterTitle, setFilterTitle] = useState('')
  const [titleSuggestions, setTitleSuggestions] = useState<string[]>([])

  const fetchRows = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params: any = { 
        page: paginationModel.page + 1, 
        per_page: paginationModel.pageSize 
      }
      if (filterTitle) params.title = filterTitle
      if (sortModel[0]) {
        const field = sortModel[0].field === 'avg_salary_mil_vnd' ? 'avg_salary' : sortModel[0].field
        params.sort_by = field
        params.sort_dir = sortModel[0].sort || 'desc'
      }
      const r = await axios.get('http://127.0.0.1:8081/api/jobs', { params, timeout: 10000 })
      setRows((r.data.items || []).map((item: any, idx: number) => ({ ...item, id: item.id || idx })))
      setRowCount(r.data.total || 0)
    } catch (e: any) {
      const msg = e.response?.data?.detail || e.message || 'Failed to fetch jobs'
      setError(`Error: ${msg}`)
      console.error('API Error:', e)
      setRows([])
      setRowCount(0)
    }
    setLoading(false)
  }, [paginationModel, sortModel, filterTitle])

  useEffect(() => { fetchRows() }, [fetchRows])

  const handleExportXLSX = async () => {
    try {
      setLoading(true)
      const r = await axios.get('http://127.0.0.1:8081/api/jobs', { params: { page: 1, per_page: 10000 } })
      const data = r.data.items || []
      const ws = XLSX.utils.json_to_sheet(data)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Jobs')
      XLSX.writeFile(wb, `jobs_export_${new Date().toISOString().split('T')[0]}.xlsx`)
    } catch (e) {
      setError('Export failed')
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'title', headerName: 'Chức vụ', width: 300, flex: 1 },
    { field: 'company', headerName: 'Công ty', width: 200 },
    { field: 'level', headerName: 'Cấp độ', width: 120 },
    { field: 'avg_salary_mil_vnd', headerName: 'Lương (triệu VND)', width: 150, type: 'number', sortable: true },
    { field: 'location', headerName: 'Địa điểm', width: 150 }
  ]

  const fetchTitleSuggestions = async (query: string) => {
    if (!query) {
      setTitleSuggestions([])
      return
    }
    try {
      const r = await axios.get(`http://127.0.0.1:8081/api/suggestions/titles?q=${query}&limit=10`)
      setTitleSuggestions(r.data.suggestions || [])
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 3 }}>
      {error && <Alert severity="error">{error}</Alert>}
      
      <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-start' }}>
        <Autocomplete
          freeSolo
          options={titleSuggestions}
          value={filterTitle}
          onChange={(_, newValue) => { setFilterTitle(newValue || ''); setPaginationModel({...paginationModel, page: 0}) }}
          onInputChange={(_, newValue) => {
            setFilterTitle(newValue)
            fetchTitleSuggestions(newValue)
          }}
          sx={{ flex: 1 }}
          renderInput={(params) => (
            <TextField
              {...params}
              placeholder="🔍 Tìm kiếm chức vụ..."
              size="small"
            />
          )}
        />
        <Button variant='outlined' onClick={fetchRows} disabled={loading}>Tìm kiếm</Button>
        <Button variant='contained' onClick={handleExportXLSX} disabled={loading}>Xuất XLSX</Button>
      </Box>

      {loading && <CircularProgress size={40} />}
      
      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          paginationModel={paginationModel}
          onPaginationModelChange={setPaginationModel}
          pageSizeOptions={[10, 20, 50, 100]}
          sortModel={sortModel}
          onSortModelChange={setSortModel}
          rowCount={rowCount}
          loading={loading}
          paginationMode="server"
          sortingMode="server"
          disableSelectionOnClick
          sx={{ 
            '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f5f5f5' },
            '& .MuiDataGrid-row:hover': { backgroundColor: '#f9f9f9' }
          }}
        />
      </Box>
    </Box>
  )
}