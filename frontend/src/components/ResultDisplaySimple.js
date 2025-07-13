import React from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
} from '@mui/material';
import { motion } from 'framer-motion';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

const ResultDisplaySimple = ({ result, domain, onRestart }) => {
  console.log('ResultDisplaySimple result:', result);
  console.log('ResultDisplaySimple domain:', domain);
  
  // 安全地獲取結果內容
  const getResultContent = () => {
    if (!result || !result.result) {
      return '暫無分析結果';
    }
    
    if (typeof result.result === 'string') {
      return result.result;
    }
    
    if (typeof result.result === 'object') {
      try {
        return JSON.stringify(result.result, null, 2);
      } catch (e) {
        return '結果格式錯誤';
      }
    }
    
    return String(result.result);
  };

  return (
    <Container maxWidth="lg">
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Box sx={{ 
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '20px',
          padding: 4,
          backdropFilter: 'blur(15px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          textAlign: 'center'
        }}>
          {/* 標題 */}
          <Typography variant="h3" sx={{ 
            color: '#ffffff',
            mb: 3,
            fontWeight: 700
          }}>
            🔮 分析結果
          </Typography>

          {/* 領域信息 */}
          <Typography variant="h5" sx={{ 
            color: 'rgba(255, 255, 255, 0.9)',
            mb: 2
          }}>
            {domain?.name || '命理'} 分析
          </Typography>

          {/* 處理時間 */}
          <Typography variant="body2" sx={{ 
            color: 'rgba(255, 255, 255, 0.7)',
            mb: 4
          }}>
            處理時間: {result?.metadata?.processing_time?.toFixed(2) || '0.00'} 秒
          </Typography>

          {/* 分析結果 */}
          <Box sx={{ 
            background: 'rgba(255, 255, 255, 0.05)',
            borderRadius: '15px',
            padding: 3,
            border: '1px solid rgba(255, 255, 255, 0.1)',
            textAlign: 'left',
            mb: 4
          }}>
            <Typography 
              variant="body1" 
              sx={{ 
                lineHeight: 1.8,
                fontSize: '1.1rem',
                whiteSpace: 'pre-wrap',
                color: 'rgba(255, 255, 255, 0.9)'
              }}
            >
              {getResultContent()}
            </Typography>
          </Box>

          {/* 重新分析按鈕 */}
          <Button
            variant="contained"
            startIcon={<RestartAltIcon />}
            onClick={onRestart}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              fontWeight: 600,
              px: 4,
              py: 1.5,
              borderRadius: '25px',
              '&:hover': {
                background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
              }
            }}
          >
            重新分析
          </Button>
        </Box>
      </motion.div>
    </Container>
  );
};

export default ResultDisplaySimple;
