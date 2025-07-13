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
// import ReactMarkdown from 'react-markdown';
// import remarkGfm from 'remark-gfm';

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

// Markdown 容器樣式
const MarkdownContainer = styled(Box)(({ theme }) => ({
  '& h1': {
    fontSize: '2rem',
    fontWeight: 700,
    color: '#ffffff',
    marginBottom: theme.spacing(2),
    marginTop: theme.spacing(3),
    borderBottom: '2px solid rgba(255, 255, 255, 0.3)',
    paddingBottom: theme.spacing(1),
  },
  '& h2': {
    fontSize: '1.5rem',
    fontWeight: 600,
    color: '#ffffff',
    marginBottom: theme.spacing(1.5),
    marginTop: theme.spacing(2.5),
    borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
    paddingBottom: theme.spacing(0.5),
  },
  '& h3': {
    fontSize: '1.25rem',
    fontWeight: 600,
    color: '#ffffff',
    marginBottom: theme.spacing(1),
    marginTop: theme.spacing(2),
  },
  '& h4, & h5, & h6': {
    fontSize: '1.1rem',
    fontWeight: 500,
    color: '#ffffff',
    marginBottom: theme.spacing(0.5),
    marginTop: theme.spacing(1.5),
  },
  '& p': {
    fontSize: '1.1rem',
    lineHeight: 1.8,
    color: 'rgba(255, 255, 255, 0.9)',
    marginBottom: theme.spacing(1.5),
  },
  '& strong': {
    fontWeight: 700,
    color: '#ffffff',
  },
  '& em': {
    fontStyle: 'italic',
    color: 'rgba(255, 255, 255, 0.95)',
  },
  '& ul, & ol': {
    paddingLeft: theme.spacing(3),
    marginBottom: theme.spacing(1.5),
  },
  '& li': {
    fontSize: '1.1rem',
    lineHeight: 1.7,
    color: 'rgba(255, 255, 255, 0.9)',
    marginBottom: theme.spacing(0.5),
  },
  '& blockquote': {
    borderLeft: '4px solid rgba(102, 126, 234, 0.6)',
    paddingLeft: theme.spacing(2),
    margin: theme.spacing(2, 0),
    fontStyle: 'italic',
    color: 'rgba(255, 255, 255, 0.8)',
    background: 'rgba(255, 255, 255, 0.05)',
    borderRadius: '0 8px 8px 0',
    padding: theme.spacing(1.5, 2),
  },
  '& code': {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    padding: '2px 6px',
    borderRadius: '4px',
    fontSize: '0.9em',
    color: '#ffffff',
  },
  '& pre': {
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    padding: theme.spacing(2),
    borderRadius: '8px',
    overflow: 'auto',
    marginBottom: theme.spacing(2),
  },
  '& pre code': {
    backgroundColor: 'transparent',
    padding: 0,
  },
}));

const ResultDisplay = ({ result, domain, onRestart }) => {
  const [expanded, setExpanded] = useState(false);

  // 調試：檢查 result 的結構
  console.log('ResultDisplay result:', result);
  console.log('ResultDisplay result.result:', result?.result);
  console.log('ResultDisplay result.result type:', typeof result?.result);

  // 安全地獲取結果內容
  const getResultContent = () => {
    if (!result || !result.result) {
      return '';
    }

    // 如果是字符串，直接返回
    if (typeof result.result === 'string') {
      return result.result;
    }

    // 如果是對象，嘗試序列化
    if (typeof result.result === 'object') {
      try {
        return JSON.stringify(result.result, null, 2);
      } catch (e) {
        console.error('無法序列化結果對象:', e);
        return '結果格式錯誤';
      }
    }

    // 其他類型，轉換為字符串
    return String(result.result);
  };

  // 簡單的 Markdown 處理函數
  const processMarkdown = (text) => {
    if (!text || typeof text !== 'string') return '';

    // 先轉義 HTML 特殊字符（除了我們要處理的 Markdown）
    let processedText = text;

    // 將 ## 轉換為 h2 標題
    processedText = processedText.replace(/^## (.+)$/gm, '<h2 class="md-h2">$1</h2>');

    // 將 ### 轉換為 h3 標題
    processedText = processedText.replace(/^### (.+)$/gm, '<h3 class="md-h3">$1</h3>');

    // 將 #### 轉換為 h4 標題
    processedText = processedText.replace(/^#### (.+)$/gm, '<h4 class="md-h4">$1</h4>');

    // 將 **text** 轉換為粗體
    processedText = processedText.replace(/\*\*(.+?)\*\*/g, '<strong class="md-strong">$1</strong>');

    // 將 *text* 轉換為斜體
    processedText = processedText.replace(/\*([^*]+?)\*/g, '<em class="md-em">$1</em>');

    // 處理有序列表
    processedText = processedText.replace(/^(\d+)\. (.+)$/gm, '<li class="md-li">$2</li>');

    // 處理無序列表
    processedText = processedText.replace(/^- (.+)$/gm, '<li class="md-li">$1</li>');

    // 將連續的 li 包裝在 ol 或 ul 中
    processedText = processedText.replace(/(<li class="md-li">.*?<\/li>)/gs, (match) => {
      // 檢查是否是有序列表（包含數字）
      if (text.match(/^\d+\./m)) {
        return `<ol class="md-ol">${match}</ol>`;
      } else {
        return `<ul class="md-ul">${match}</ul>`;
      }
    });

    // 將雙換行轉換為段落分隔
    processedText = processedText.replace(/\n\n/g, '</p><p class="md-p">');

    // 將單換行轉換為 br
    processedText = processedText.replace(/\n/g, '<br>');

    // 包裝在段落中
    if (!processedText.includes('<h2') && !processedText.includes('<h3') && !processedText.includes('<ol') && !processedText.includes('<ul')) {
      processedText = '<p class="md-p">' + processedText + '</p>';
    }

    return processedText;
  };

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
    const content = getResultContent();
    if (!content) {
      console.warn('沒有可下載的內容');
      return;
    }

    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `紫微斗數分析_${domain?.name || '命理'}_${new Date().toLocaleDateString()}.txt`;
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
                {domain?.icon || '🔮'}
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
                您的{domain?.name || '命理'}分析結果
              </Typography>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              <Chip
                label={`分析完成 • 處理時間: ${result.metadata?.processing_time?.toFixed(2) || '0.00'}秒`}
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

            <MarkdownContainer sx={{
              background: 'rgba(255, 255, 255, 0.05)',
              borderRadius: '15px',
              padding: 3,
              border: '1px solid rgba(255, 255, 255, 0.1)',
              '& .md-h2': {
                fontSize: '1.5rem',
                fontWeight: 600,
                color: '#ffffff',
                marginBottom: '12px',
                marginTop: '20px',
                borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
                paddingBottom: '4px',
                display: 'block',
              },
              '& .md-h3': {
                fontSize: '1.25rem',
                fontWeight: 600,
                color: '#ffffff',
                marginBottom: '8px',
                marginTop: '16px',
                display: 'block',
              },
              '& .md-h4': {
                fontSize: '1.1rem',
                fontWeight: 600,
                color: '#ffffff',
                marginBottom: '6px',
                marginTop: '12px',
                display: 'block',
              },
              '& .md-p': {
                fontSize: '1.1rem',
                lineHeight: 1.8,
                color: 'rgba(255, 255, 255, 0.9)',
                marginBottom: '12px',
                display: 'block',
              },
              '& .md-strong': {
                fontWeight: 700,
                color: '#ffffff',
              },
              '& .md-em': {
                fontStyle: 'italic',
                color: 'rgba(255, 255, 255, 0.95)',
              },
              '& .md-ol, & .md-ul': {
                paddingLeft: '24px',
                marginBottom: '12px',
                color: 'rgba(255, 255, 255, 0.9)',
              },
              '& .md-li': {
                fontSize: '1.1rem',
                lineHeight: 1.7,
                marginBottom: '4px',
                color: 'rgba(255, 255, 255, 0.9)',
              },
            }}>
              <div dangerouslySetInnerHTML={{
                __html: processMarkdown(getResultContent()) || '暫無分析結果'
              }} />
            </MarkdownContainer>
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
                      {result.metadata?.processing_time?.toFixed(2) || '0.00'} 秒
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      分析領域
                    </Typography>
                    <Typography variant="body1">
                      {domain?.name || '未知領域'}
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
