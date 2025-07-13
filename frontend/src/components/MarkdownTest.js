import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const MarkdownTest = ({ onBack }) => {
  const testMarkdown = `## 命盤整體印象

在這個充滿希望的時刻，您在感情運勢上的整體評分為7分，這意味著您的愛情運勢相當不錯，充滿了潛力與機會。

### 詳細分析

在您的命盤中，夫妻宮的主星顯示出您對於感情的渴望與追求。您擁有**良好的情感表達能力**，這使得您能夠在關係中創造出浪漫的氛圍。

### 實用的人生指導

為了讓您的感情生活更加美好，以下是一些具體的建議：

1. **積極參加社交活動**：擴展人際圈，增加遇見理想伴侶的機會
2. **保持開放心態**：對新的關係保持開放和積極的態度
3. **提升自我修養**：持續學習和成長，讓自己更有魅力`;

  return (
    <Box sx={{ 
      p: 4, 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      minHeight: '100vh'
    }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ color: 'white' }}>
          Markdown 測試
        </Typography>
        <Button
          variant="outlined"
          onClick={() => window.location.reload()}
          sx={{ color: 'white', borderColor: 'white' }}
        >
          返回主頁
        </Button>
      </Box>
      
      <Box sx={{ 
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '15px',
        padding: 3,
        border: '1px solid rgba(255, 255, 255, 0.2)'
      }}>
        <Box sx={{
          '& h1': {
            fontSize: '2rem',
            fontWeight: 700,
            color: '#ffffff',
            marginBottom: '16px',
            marginTop: '24px',
            borderBottom: '2px solid rgba(255, 255, 255, 0.3)',
            paddingBottom: '8px',
          },
          '& h2': {
            fontSize: '1.5rem',
            fontWeight: 600,
            color: '#ffffff',
            marginBottom: '12px',
            marginTop: '20px',
            borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
            paddingBottom: '4px',
          },
          '& h3': {
            fontSize: '1.25rem',
            fontWeight: 600,
            color: '#ffffff',
            marginBottom: '8px',
            marginTop: '16px',
          },
          '& p': {
            fontSize: '1.1rem',
            lineHeight: 1.8,
            color: 'rgba(255, 255, 255, 0.9)',
            marginBottom: '12px',
          },
          '& strong': {
            fontWeight: 700,
            color: '#ffffff',
          },
          '& ol, & ul': {
            paddingLeft: '24px',
            marginBottom: '12px',
            color: 'rgba(255, 255, 255, 0.9)',
          },
          '& li': {
            fontSize: '1.1rem',
            lineHeight: 1.7,
            marginBottom: '4px',
          },
        }}>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {testMarkdown}
          </ReactMarkdown>
        </Box>
      </Box>
    </Box>
  );
};

export default MarkdownTest;
