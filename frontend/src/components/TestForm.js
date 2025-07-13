import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Box,
  Card,
  CardContent,
  CardActionArea,
  Chip,
} from '@mui/material';

const TestForm = () => {
  const [formData, setFormData] = useState({
    gender: '',
    birth_year: '',
    birth_month: '',
    birth_day: '',
    birth_hour: '',
  });

  const [selectedDomain, setSelectedDomain] = useState(null);

  // 默認數據
  const domains = [
    {
      id: "love",
      name: "愛情感情",
      description: "專精於感情運勢、桃花運、婚姻分析",
      icon: "💕"
    },
    {
      id: "wealth", 
      name: "財富事業",
      description: "專精於財運分析、事業發展、投資理財",
      icon: "💰"
    },
    {
      id: "comprehensive",
      name: "綜合命盤", 
      description: "專精於全面命盤分析、人生格局預測",
      icon: "🔮"
    }
  ];

  const birthHours = [
    {id: "子", name: "子時", time: "23:00-01:00"},
    {id: "丑", name: "丑時", time: "01:00-03:00"},
    {id: "寅", name: "寅時", time: "03:00-05:00"},
    {id: "卯", name: "卯時", time: "05:00-07:00"},
    {id: "辰", name: "辰時", time: "07:00-09:00"},
    {id: "巳", name: "巳時", time: "09:00-11:00"},
    {id: "午", name: "午時", time: "11:00-13:00"},
    {id: "未", name: "未時", time: "13:00-15:00"},
    {id: "申", name: "申時", time: "15:00-17:00"},
    {id: "酉", name: "酉時", time: "17:00-19:00"},
    {id: "戌", name: "戌時", time: "19:00-21:00"},
    {id: "亥", name: "亥時", time: "21:00-23:00"}
  ];

  const handleInputChange = (field) => (event) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('表單數據:', formData);
    console.log('選擇的領域:', selectedDomain);
    alert(`表單提交成功！\n性別: ${formData.gender}\n年份: ${formData.birth_year}\n時辰: ${formData.birth_hour}\n領域: ${selectedDomain?.name || '未選擇'}`);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper sx={{ p: 4, background: 'rgba(255, 255, 255, 0.1)', backdropFilter: 'blur(10px)' }}>
        <Typography variant="h4" gutterBottom textAlign="center">
          🧪 測試表單
        </Typography>

        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            {/* 性別 */}
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>性別</InputLabel>
                <Select
                  value={formData.gender}
                  onChange={handleInputChange('gender')}
                  label="性別"
                >
                  <MenuItem value="男">👨 男</MenuItem>
                  <MenuItem value="女">👩 女</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            {/* 出生年份 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="出生年份"
                type="number"
                value={formData.birth_year}
                onChange={handleInputChange('birth_year')}
                inputProps={{ min: 1900, max: 2100 }}
              />
            </Grid>

            {/* 出生月份 */}
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth>
                <InputLabel>出生月份</InputLabel>
                <Select
                  value={formData.birth_month}
                  onChange={handleInputChange('birth_month')}
                  label="出生月份"
                >
                  {Array.from({ length: 12 }, (_, i) => (
                    <MenuItem key={i + 1} value={i + 1}>
                      {i + 1} 月
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* 出生日期 */}
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth>
                <InputLabel>出生日期</InputLabel>
                <Select
                  value={formData.birth_day}
                  onChange={handleInputChange('birth_day')}
                  label="出生日期"
                >
                  {Array.from({ length: 31 }, (_, i) => (
                    <MenuItem key={i + 1} value={i + 1}>
                      {i + 1} 日
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* 出生時辰 */}
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth>
                <InputLabel>出生時辰</InputLabel>
                <Select
                  value={formData.birth_hour}
                  onChange={handleInputChange('birth_hour')}
                  label="出生時辰"
                >
                  {birthHours.map((hour) => (
                    <MenuItem key={hour.id} value={hour.id}>
                      {hour.name} ({hour.time})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          {/* 分析領域選擇 */}
          <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 3 }}>
            🎯 選擇分析領域
          </Typography>

          <Grid container spacing={2}>
            {domains.map((domain) => (
              <Grid item xs={12} sm={4} key={domain.id}>
                <Card 
                  sx={{ 
                    cursor: 'pointer',
                    border: selectedDomain?.id === domain.id ? '2px solid #1976d2' : '1px solid rgba(255,255,255,0.2)',
                    background: selectedDomain?.id === domain.id ? 'rgba(25, 118, 210, 0.1)' : 'rgba(255,255,255,0.05)',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: 3,
                    }
                  }}
                  onClick={() => setSelectedDomain(domain)}
                >
                  <CardActionArea>
                    <CardContent sx={{ textAlign: 'center', py: 3 }}>
                      <Typography variant="h2" sx={{ mb: 1 }}>
                        {domain.icon}
                      </Typography>
                      <Typography variant="h6" gutterBottom>
                        {domain.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {domain.description}
                      </Typography>
                      {selectedDomain?.id === domain.id && (
                        <Chip 
                          label="已選擇" 
                          color="primary" 
                          size="small" 
                          sx={{ mt: 1 }}
                        />
                      )}
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* 提交按鈕 */}
          <Box textAlign="center" mt={4}>
            <Button
              type="submit"
              variant="contained"
              size="large"
              sx={{ 
                borderRadius: '25px',
                px: 4,
                py: 1.5,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              }}
            >
              🔮 測試提交
            </Button>
          </Box>

          {/* 調試信息 */}
          <Box mt={4} p={2} sx={{ background: 'rgba(0,0,0,0.2)', borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom>調試信息：</Typography>
            <Typography variant="body2">
              表單數據: {JSON.stringify(formData, null, 2)}
            </Typography>
            <Typography variant="body2" mt={1}>
              選擇的領域: {selectedDomain ? selectedDomain.name : '未選擇'}
            </Typography>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default TestForm;
