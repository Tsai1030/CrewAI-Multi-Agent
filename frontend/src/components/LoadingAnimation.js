import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  LinearProgress,
  CircularProgress
} from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { styled } from '@mui/material/styles';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(6),
  background: 'rgba(255, 255, 255, 0.1)',
  backdropFilter: 'blur(15px)',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  borderRadius: '20px',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
  textAlign: 'center',
  minHeight: '400px',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
}));

const FloatingIcon = styled(motion.div)(({ theme }) => ({
  fontSize: '4rem',
  marginBottom: theme.spacing(3),
}));

const LoadingAnimation = ({ domain }) => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);

  const loadingSteps = [
    { text: '正在初始化 AI 系統...', icon: '🤖' },
    { text: '載入紫微斗數知識庫...', icon: '📚' },
    { text: 'Multi-Agent 開始協作分析...', icon: '🧠' },
    { text: '整合分析結果...', icon: '⚡' },
    { text: '生成專業報告...', icon: '📊' },
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prevProgress) => {
        const newProgress = prevProgress + 2;
        
        // 更新步驟
        const stepIndex = Math.floor(newProgress / 20);
        if (stepIndex !== currentStep && stepIndex < loadingSteps.length) {
          setCurrentStep(stepIndex);
        }
        
        return newProgress >= 100 ? 100 : newProgress;
      });
    }, 100);

    return () => clearInterval(timer);
  }, [currentStep, loadingSteps.length]);

  return (
    <Container maxWidth="md">
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6 }}
      >
        <StyledPaper elevation={0}>
          {/* 領域圖標 */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          >
            <Typography variant="h1" sx={{ mb: 2 }}>
              {domain?.icon || '🔮'}
            </Typography>
          </motion.div>

          {/* 標題 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Typography 
              variant="h4" 
              gutterBottom
              sx={{ 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontWeight: 700,
                mb: 1
              }}
            >
              正在分析您的{domain?.name || '命盤'}
            </Typography>
          </motion.div>

          {/* 浮動圖標 */}
          <AnimatePresence mode="wait">
            <FloatingIcon
              key={currentStep}
              initial={{ opacity: 0, y: 20, scale: 0.8 }}
              animate={{ 
                opacity: 1, 
                y: 0, 
                scale: 1,
                rotate: [0, 5, -5, 0]
              }}
              exit={{ opacity: 0, y: -20, scale: 0.8 }}
              transition={{ 
                duration: 0.5,
                rotate: {
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }
              }}
            >
              {loadingSteps[currentStep]?.icon}
            </FloatingIcon>
          </AnimatePresence>

          {/* 當前步驟文字 */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Typography 
                variant="h6" 
                color="text.secondary" 
                sx={{ mb: 4, minHeight: '2rem' }}
              >
                {loadingSteps[currentStep]?.text}
              </Typography>
            </motion.div>
          </AnimatePresence>

          {/* 進度條 */}
          <Box sx={{ width: '100%', mb: 3 }}>
            <motion.div
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ delay: 0.6, duration: 0.8 }}
            >
              <LinearProgress 
                variant="determinate" 
                value={progress} 
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  '& .MuiLinearProgress-bar': {
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    borderRadius: 4,
                  }
                }}
              />
            </motion.div>
          </Box>

          {/* 進度百分比 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            <Typography variant="body1" color="text.secondary">
              {Math.round(progress)}% 完成
            </Typography>
          </motion.div>

          {/* 旋轉的裝飾元素 */}
          <Box sx={{ position: 'absolute', top: 20, right: 20 }}>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
            >
              <CircularProgress 
                size={40} 
                thickness={2}
                sx={{ 
                  color: 'rgba(102, 126, 234, 0.6)',
                  opacity: 0.7
                }}
              />
            </motion.div>
          </Box>

          {/* 底部提示 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.2 }}
            style={{ marginTop: 'auto' }}
          >
            <Typography 
              variant="body2" 
              color="text.secondary"
              sx={{ 
                fontStyle: 'italic',
                opacity: 0.8
              }}
            >
              AI 正在運用深度學習技術為您進行精準分析...
            </Typography>
          </motion.div>
        </StyledPaper>
      </motion.div>
    </Container>
  );
};

export default LoadingAnimation;
