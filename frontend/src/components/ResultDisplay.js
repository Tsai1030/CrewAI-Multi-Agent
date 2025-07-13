import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Divider,
  Chip,
  Card,
  CardContent,
  Grid,
  IconButton,
  Collapse,
} from '@mui/material';
import { motion } from 'framer-motion';
import { styled } from '@mui/material/styles';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import ShareIcon from '@mui/icons-material/Share';
import DownloadIcon from '@mui/icons-material/Download';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  background: 'rgba(255, 255, 255, 0.1)',
  backdropFilter: 'blur(15px)',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  borderRadius: '20px',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
  marginBottom: theme.spacing(3),
}));

const ResultCard = styled(Card)(({ theme }) => ({
  background: 'rgba(255, 255, 255, 0.05)',
  backdropFilter: 'blur(10px)',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  borderRadius: '15px',
  marginBottom: theme.spacing(2),
}));

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

const ResultDisplay = ({ result, domain, onRestart }) => {
  const [expanded, setExpanded] = useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const handleShare = () => {
    // 實現分享功能
    if (navigator.share) {
      navigator.share({
        title: '我的紫微斗數分析結果',
        text: '來看看我的命理分析結果！',
        url: window.location.href,
      });
    }
  };

  const handleDownload = () => {
    // 實現下載功能
    const element = document.createElement('a');
    const file = new Blob([result.result], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `紫微斗數分析_${domain.name}_${new Date().toLocaleDateString()}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <Container maxWidth="lg">
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        {/* 標題區域 */}
        <StyledPaper elevation={0}>
          <Box textAlign="center" mb={3}>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            >
              <Typography variant="h1" sx={{ mb: 2 }}>
                {domain.icon}
              </Typography>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Typography 
                variant="h3" 
                gutterBottom
                sx={{ 
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontWeight: 700,
                  mb: 1
                }}
              >
                您的{domain.name}分析結果
              </Typography>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              <Chip 
                label={`分析完成 • 處理時間: ${result.metadata?.processing_time?.toFixed(2)}秒`}
                color="primary"
                sx={{ mb: 2 }}
              />
            </motion.div>

            {/* 操作按鈕 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
            >
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                <Button
                  variant="outlined"
                  startIcon={<ShareIcon />}
                  onClick={handleShare}
                  sx={{ borderRadius: '20px' }}
                >
                  分享結果
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={handleDownload}
                  sx={{ borderRadius: '20px' }}
                >
                  下載報告
                </Button>
                <Button
                  variant="contained"
                  startIcon={<RestartAltIcon />}
                  onClick={onRestart}
                  sx={{ 
                    borderRadius: '20px',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  }}
                >
                  重新分析
                </Button>
              </Box>
            </motion.div>
          </Box>
        </StyledPaper>

        {/* 分析結果內容 */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <StyledPaper elevation={0}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
              📖 詳細分析報告
            </Typography>

            <Box sx={{ 
              background: 'rgba(255, 255, 255, 0.05)',
              borderRadius: '15px',
              padding: 3,
              border: '1px solid rgba(255, 255, 255, 0.1)'
            }}>
              <Typography 
                variant="body1" 
                sx={{ 
                  lineHeight: 1.8,
                  fontSize: '1.1rem',
                  whiteSpace: 'pre-wrap',
                  color: 'text.primary'
                }}
              >
                {result.result}
              </Typography>
            </Box>
          </StyledPaper>
        </motion.div>

        {/* 技術詳情（可展開） */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <ResultCard>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                  🔧 技術詳情
                </Typography>
                <ExpandMore
                  expand={expanded}
                  onClick={handleExpandClick}
                  aria-expanded={expanded}
                  aria-label="顯示更多"
                >
                  <ExpandMoreIcon />
                </ExpandMore>
              </Box>
              
              <Collapse in={expanded} timeout="auto" unmountOnExit>
                <Divider sx={{ my: 2 }} />
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      分析模型
                    </Typography>
                    <Typography variant="body1">
                      Multi-Agent AI 系統
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      處理時間
                    </Typography>
                    <Typography variant="body1">
                      {result.metadata?.processing_time?.toFixed(2)} 秒
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      分析領域
                    </Typography>
                    <Typography variant="body1">
                      {domain.name}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      輸出格式
                    </Typography>
                    <Typography variant="body1">
                      JSON 轉論述格式
                    </Typography>
                  </Grid>
                </Grid>
              </Collapse>
            </CardContent>
          </ResultCard>
        </motion.div>

        {/* 免責聲明 */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0 }}
        >
          <Box sx={{ 
            textAlign: 'center', 
            mt: 4, 
            p: 2, 
            background: 'rgba(255, 255, 255, 0.05)',
            borderRadius: '10px',
            border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
              ⚠️ 本分析結果僅供參考，不應作為人生重大決策的唯一依據。
              命運掌握在自己手中，積極面對生活才是最重要的。
            </Typography>
          </Box>
        </motion.div>
      </motion.div>
    </Container>
  );
};

export default ResultDisplay;
