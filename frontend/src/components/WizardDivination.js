import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  LinearProgress,
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
  minHeight: '500px',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  position: 'relative',
  overflow: 'hidden',
}));

const WizardContainer = styled(Box)(({ theme }) => ({
  position: 'relative',
  width: '200px',
  height: '200px',
  margin: '0 auto',
  marginBottom: theme.spacing(3),
  [theme.breakpoints.down('sm')]: {
    width: '150px',
    height: '150px',
  },
}));

const FloatingIcon = styled(motion.img)(({ theme }) => ({
  position: 'absolute',
  width: '60px',
  height: '60px',
  borderRadius: '50%',
  background: 'rgba(255, 255, 255, 0.1)',
  padding: '8px',
  backdropFilter: 'blur(10px)',
}));

const WizardIcon = styled(motion.img)(({ theme }) => ({
  width: '120px',
  height: '120px',
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  filter: 'drop-shadow(0 0 20px rgba(102, 126, 234, 0.6))',
  [theme.breakpoints.down('sm')]: {
    width: '90px',
    height: '90px',
  },
}));

const MagicParticle = styled(motion.div)(({ theme }) => ({
  position: 'absolute',
  width: '4px',
  height: '4px',
  background: 'linear-gradient(45deg, #667eea, #764ba2)',
  borderRadius: '50%',
  boxShadow: '0 0 10px rgba(102, 126, 234, 0.8)',
}));

const WizardDivination = ({ domain }) => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [particles, setParticles] = useState([]);

  const divinationSteps = [
    { text: '巫師正在準備神秘的占卜工具...', duration: 25000, sound: '🔮✨' },
    { text: '施展古老魔法連接天體星象...', duration: 30000, sound: '🌟⭐' },
    { text: '深入解讀紫微斗數的神秘密碼...', duration: 40000, sound: '📜🔍' },
    { text: 'Multi-Agent AI 智者們正在激烈討論...', duration: 35000, sound: '🤖💭' },
    { text: '巫師正在整合來自星空的預言...', duration: 30000, sound: '🌌🔮' },
    { text: '完成您專屬的神秘預言書...', duration: 30000, sound: '📖✨' },
  ];

  // 生成魔法粒子
  useEffect(() => {
    const generateParticles = () => {
      const newParticles = [];
      for (let i = 0; i < 15; i++) {
        newParticles.push({
          id: i,
          x: Math.random() * 400,
          y: Math.random() * 400,
          delay: Math.random() * 2,
        });
      }
      setParticles(newParticles);
    };

    generateParticles();
  }, []);

  // 進度控制
  useEffect(() => {
    let totalDuration = 0;

    // 計算總時間
    divinationSteps.forEach(step => {
      totalDuration += step.duration;
    });

    const timer = setInterval(() => {
      setProgress((prevProgress) => {
        const newProgress = prevProgress + (100 / totalDuration) * 100;
        
        // 更新步驟
        let stepIndex = 0;
        let accumulatedTime = 0;
        
        for (let i = 0; i < divinationSteps.length; i++) {
          accumulatedTime += divinationSteps[i].duration;
          if ((newProgress / 100) * totalDuration <= accumulatedTime) {
            stepIndex = i;
            break;
          }
        }
        
        if (stepIndex !== currentStep) {
          setCurrentStep(stepIndex);
        }
        
        return newProgress >= 100 ? 100 : newProgress;
      });
    }, 100);

    return () => clearInterval(timer);
  }, [currentStep, divinationSteps]);

  return (
    <Container maxWidth="md">
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8 }}
      >
        <StyledPaper elevation={0}>
          {/* 魔法粒子背景 */}
          {particles.map((particle) => (
            <MagicParticle
              key={particle.id}
              initial={{ 
                x: particle.x, 
                y: particle.y, 
                opacity: 0,
                scale: 0 
              }}
              animate={{ 
                x: particle.x + Math.sin(Date.now() * 0.001 + particle.id) * 20,
                y: particle.y + Math.cos(Date.now() * 0.001 + particle.id) * 20,
                opacity: [0, 1, 0],
                scale: [0, 1, 0]
              }}
              transition={{ 
                duration: 3,
                repeat: Infinity,
                delay: particle.delay,
                ease: "easeInOut"
              }}
            />
          ))}

          {/* 領域圖標 */}
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          >
            <Typography variant="h1" sx={{ mb: 2, fontSize: '4rem' }}>
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
                mb: 3,
                fontSize: { xs: '1.5rem', sm: '2rem', md: '2.5rem' },
                textAlign: 'center',
                lineHeight: 1.2
              }}
            >
              🧙‍♂️ 神秘占卜進行中...
            </Typography>
          </motion.div>

          {/* 巫師和魔法工具動畫 */}
          <WizardContainer>
            {/* 主巫師 */}
            <WizardIcon
              src="/wizard_icon/wizard.png"
              alt="巫師"
              animate={{ 
                y: [0, -10, 0],
                rotate: [0, 2, -2, 0]
              }}
              transition={{ 
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />

            {/* 魔法帽 */}
            <FloatingIcon
              src="/wizard_icon/wizard-hat.png"
              alt="魔法帽"
              style={{ top: '-20px', left: '20px' }}
              animate={{ 
                rotate: 360,
                scale: [1, 1.1, 1]
              }}
              transition={{ 
                rotate: { duration: 8, repeat: Infinity, ease: "linear" },
                scale: { duration: 2, repeat: Infinity, ease: "easeInOut" }
              }}
            />

            {/* 魔法棒 */}
            <FloatingIcon
              src="/wizard_icon/magic-wand.png"
              alt="魔法棒"
              style={{ top: '60px', right: '-20px' }}
              animate={{ 
                rotate: [0, 15, -15, 0],
                y: [0, -5, 5, 0]
              }}
              transition={{ 
                duration: 2.5,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />

            {/* 水晶球 */}
            <FloatingIcon
              src="/wizard_icon/crystal-ball.png"
              alt="水晶球"
              style={{ bottom: '-10px', left: '-20px' }}
              animate={{ 
                scale: [1, 1.2, 1],
                boxShadow: [
                  '0 0 20px rgba(102, 126, 234, 0.4)',
                  '0 0 40px rgba(102, 126, 234, 0.8)',
                  '0 0 20px rgba(102, 126, 234, 0.4)'
                ]
              }}
              transition={{ 
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />
          </WizardContainer>

          {/* 當前步驟文字 */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <Typography
                variant="h6"
                sx={{
                  color: '#ffffff', // 改為白色
                  mb: 2,
                  minHeight: '2rem',
                  fontStyle: 'italic',
                  textShadow: '0 2px 4px rgba(0, 0, 0, 0.5)' // 增強陰影對比
                }}
              >
                ✨ {divinationSteps[currentStep]?.text}
              </Typography>

              {/* 音效提示 */}
              <motion.div
                key={`sound-${currentStep}`}
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: [0, 1.2, 1], opacity: [0, 1, 0.7] }}
                transition={{ duration: 1, ease: "easeOut" }}
              >
                <Typography
                  variant="h4"
                  sx={{
                    mb: 2,
                    filter: 'drop-shadow(0 0 10px rgba(102, 126, 234, 0.8))'
                  }}
                >
                  {divinationSteps[currentStep]?.sound}
                </Typography>
              </motion.div>
            </motion.div>
          </AnimatePresence>

          {/* 魔法進度條 */}
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
                  height: 12,
                  borderRadius: 6,
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  '& .MuiLinearProgress-bar': {
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    borderRadius: 6,
                    boxShadow: '0 0 20px rgba(102, 126, 234, 0.6)',
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
            <Typography 
              variant="h6" 
              sx={{ 
                color: 'primary.main',
                fontWeight: 600,
                textShadow: '0 0 10px rgba(102, 126, 234, 0.6)'
              }}
            >
              {Math.round(progress)}% 完成
            </Typography>
          </motion.div>

          {/* 底部提示 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.2 }}
            style={{ marginTop: 'auto' }}
          >
            <Typography
              variant="body2"
              sx={{
                color: '#ffffff', // 改為白色
                fontStyle: 'italic',
                opacity: 1, // 提高透明度讓白色更明顯
                mt: 3,
                textShadow: '0 2px 4px rgba(0, 0, 0, 0.5)' // 添加陰影增強對比
              }}
            >
              🌟 古老的智慧與現代 AI 正在為您揭示命運的奧秘...
            </Typography>
          </motion.div>
        </StyledPaper>
      </motion.div>
    </Container>
  );
};

export default WizardDivination;
