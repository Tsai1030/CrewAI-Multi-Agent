import React, { useState, useEffect } from 'react';
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
  FormControlLabel,
  Switch,
} from '@mui/material';
import { motion } from 'framer-motion';
import { styled } from '@mui/material/styles';

// 自定義樣式組件
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  background: 'rgba(255, 255, 255, 0.1)',
  backdropFilter: 'blur(15px)',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  borderRadius: '20px',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
}));

const DomainCard = styled(Card)(({ theme, selected }) => ({
  background: selected 
    ? 'linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%)'
    : 'rgba(255, 255, 255, 0.05)',
  backdropFilter: 'blur(10px)',
  border: selected 
    ? '2px solid rgba(102, 126, 234, 0.8)'
    : '1px solid rgba(255, 255, 255, 0.1)',
  borderRadius: '15px',
  transition: 'all 0.3s ease',
  cursor: 'pointer',
  height: '100%',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.4)',
    border: '2px solid rgba(102, 126, 234, 0.6)',
  },
}));

const SubmitButton = styled(Button)(({ theme }) => ({
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  borderRadius: '25px',
  padding: '12px 40px',
  fontSize: '1.1rem',
  fontWeight: 600,
  textTransform: 'none',
  boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
  '&:hover': {
    background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
    transform: 'translateY(-2px)',
    boxShadow: '0 6px 20px rgba(102, 126, 234, 0.6)',
  },
}));

const ZiweiForm = ({ onSubmit, useWizardAnimation, setUseWizardAnimation }) => {
  const [formData, setFormData] = useState({
    gender: '',
    birth_year: '',
    birth_month: '',
    birth_day: '',
    birth_hour: '',
  });

  const [selectedDomain, setSelectedDomain] = useState(null);
  const [domains, setDomains] = useState([
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
  ]);
  const [birthHours, setBirthHours] = useState([
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
  ]);
  const [errors, setErrors] = useState({});

  // 獲取領域和時辰數據（可選，如果後端可用的話）
  useEffect(() => {
    // 嘗試從後端獲取數據，如果失敗則使用默認數據
    fetchDomains();
    fetchBirthHours();
  }, []);

  const fetchDomains = async () => {
    try {
      const response = await fetch('http://localhost:8000/domains');
      if (response.ok) {
        const data = await response.json();
        setDomains(data.domains);
        console.log('✅ 成功從後端獲取領域數據');
      }
    } catch (error) {
      console.log('🔄 使用默認領域數據（後端未連接）');
      // 已經有默認數據，不需要額外處理
    }
  };

  const fetchBirthHours = async () => {
    try {
      const response = await fetch('http://localhost:8000/birth-hours');
      if (response.ok) {
        const data = await response.json();
        setBirthHours(data.hours);
        console.log('✅ 成功從後端獲取時辰數據');
      }
    } catch (error) {
      console.log('🔄 使用默認時辰數據（後端未連接）');
      // 已經有默認數據，不需要額外處理
    }
  };

  // 處理表單變更
  const handleInputChange = (field) => (event) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
    
    // 清除錯誤
    if (errors[field]) {
      setErrors({
        ...errors,
        [field]: '',
      });
    }
  };

  // 驗證表單
  const validateForm = () => {
    const newErrors = {};

    if (!formData.gender) newErrors.gender = '請選擇性別';
    if (!formData.birth_year) newErrors.birth_year = '請輸入出生年份';
    if (!formData.birth_month) newErrors.birth_month = '請選擇出生月份';
    if (!formData.birth_day) newErrors.birth_day = '請選擇出生日期';
    if (!formData.birth_hour) newErrors.birth_hour = '請選擇出生時辰';
    if (!selectedDomain) newErrors.domain = '請選擇分析領域';

    // 年份範圍驗證
    const year = parseInt(formData.birth_year);
    if (year && (year < 1900 || year > 2100)) {
      newErrors.birth_year = '年份必須在 1900-2100 之間';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 提交表單
  const handleSubmit = (event) => {
    event.preventDefault();
    
    if (validateForm()) {
      onSubmit(formData, selectedDomain);
    }
  };

  return (
    <Container maxWidth="md">
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <StyledPaper elevation={0}>
          <Box textAlign="center" mb={4}>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
            >
              <Typography
                variant="h3"
                component="h1"
                gutterBottom
                sx={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontWeight: 700,
                  mb: 2,
                  fontSize: { xs: '1.8rem', sm: '2.5rem', md: '3rem' },
                  textAlign: 'center',
                  lineHeight: 1.2
                }}
              >
                🌟 紫微斗數 AI 系統
              </Typography>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              <Typography variant="h6" color="text.secondary">
                輸入您的出生資訊，讓 AI 為您解析命運密碼
              </Typography>
            </motion.div>
          </Box>

          <form onSubmit={handleSubmit}>
            {/* 基本資訊 */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
                📋 基本資訊
              </Typography>
            </motion.div>

            <Grid container spacing={3}>
              {/* 性別 */}
              <Grid item xs={12} sm={6}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                >
                  <FormControl fullWidth error={!!errors.gender}>
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
                </motion.div>
              </Grid>

              {/* 出生年份 */}
              <Grid item xs={12} sm={6}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                >
                  <TextField
                    fullWidth
                    label="出生年份"
                    type="number"
                    value={formData.birth_year}
                    onChange={handleInputChange('birth_year')}
                    error={!!errors.birth_year}
                    helperText={errors.birth_year}
                    inputProps={{ min: 1900, max: 2100 }}
                  />
                </motion.div>
              </Grid>

              {/* 出生月份 */}
              <Grid item xs={12} sm={4}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 }}
                >
                  <FormControl fullWidth error={!!errors.birth_month}>
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
                </motion.div>
              </Grid>

              {/* 出生日期 */}
              <Grid item xs={12} sm={4}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 }}
                >
                  <FormControl fullWidth error={!!errors.birth_day}>
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
                </motion.div>
              </Grid>

              {/* 出生時辰 */}
              <Grid item xs={12} sm={4}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.9 }}
                >
                  <FormControl fullWidth error={!!errors.birth_hour}>
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
                </motion.div>
              </Grid>
            </Grid>

            {/* 分析領域選擇 */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1.0 }}
            >
              <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 3, fontWeight: 600 }}>
                🎯 選擇分析領域
              </Typography>
            </motion.div>

            <Grid container spacing={2}>
              {domains.map((domain, index) => (
                <Grid item xs={12} sm={4} key={domain.id}>
                  <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 1.1 + index * 0.1 }}
                  >
                    <DomainCard 
                      selected={selectedDomain?.id === domain.id}
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
                    </DomainCard>
                  </motion.div>
                </Grid>
              ))}
            </Grid>

            {errors.domain && (
              <Typography color="error" variant="body2" sx={{ mt: 1, textAlign: 'center' }}>
                {errors.domain}
              </Typography>
            )}

            {/* 動畫風格選擇 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.4 }}
            >
              <Box sx={{ mt: 3, textAlign: 'center' }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={useWizardAnimation}
                      onChange={(e) => setUseWizardAnimation(e.target.checked)}
                      color="primary"
                    />
                  }
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2">
                        {useWizardAnimation ? '🧙‍♂️ 巫師占卜動畫' : '⚡ 科技載入動畫'}
                      </Typography>
                    </Box>
                  }
                  sx={{
                    '& .MuiFormControlLabel-label': {
                      color: 'text.secondary',
                      fontSize: '0.9rem'
                    }
                  }}
                />
              </Box>
            </motion.div>

            {/* 提交按鈕 */}
            <Box textAlign="center" mt={4}>
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.5 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <SubmitButton
                  type="submit"
                  variant="contained"
                  size="large"
                  startIcon={<span>🔮</span>}
                >
                  開始 AI 命理分析
                </SubmitButton>
              </motion.div>
            </Box>
          </form>
        </StyledPaper>
      </motion.div>
    </Container>
  );
};

export default ZiweiForm;
