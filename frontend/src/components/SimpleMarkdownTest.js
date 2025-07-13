import React from 'react';
import { Box, Typography, Button } from '@mui/material';

const SimpleMarkdownTest = () => {
  // 模擬處理 Markdown 的簡單函數
  const processMarkdown = (text) => {
    // 將 ## 轉換為 h2 標題
    text = text.replace(/^## (.+)$/gm, '<h2 class="md-h2">$1</h2>');
    
    // 將 ### 轉換為 h3 標題
    text = text.replace(/^### (.+)$/gm, '<h3 class="md-h3">$1</h3>');
    
    // 將 **text** 轉換為粗體
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong class="md-strong">$1</strong>');
    
    // 將換行轉換為段落
    text = text.replace(/\n\n/g, '</p><p class="md-p">');
    text = '<p class="md-p">' + text + '</p>';
    
    // 處理列表項
    text = text.replace(/^(\d+)\. (.+)$/gm, '<li class="md-li">$2</li>');
    text = text.replace(/(<li class="md-li">.*<\/li>)/s, '<ol class="md-ol">$1</ol>');
    
    return text;
  };

  const testMarkdown = `## 命盤整體印象

在這個充滿希望的時刻，您在感情運勢上的整體評分為7分，這意味著您的愛情運勢相當不錯，充滿了潛力與機會。根據紫微斗數的分析，您的命盤顯示出對情感的深刻理解和良好的表達能力，這使得您在建立和維持關係方面具備了優勢。

### 詳細分析

在您的命盤中，夫妻宮的主星顯示出您對於感情的渴望與追求。您擁有**良好的情感表達能力**，這使得您能夠在關係中創造出浪漫的氛圍，讓伴侶感受到您的真誠與愛意。您對伴侶有著強烈的**保護欲**，這讓您在感情中展現出無私的一面，願意為對方付出。

### 實用的人生指導

為了讓您的感情生活更加美好，以下是一些具體的建議，幫助您在愛情的旅程中更加順利：

1. **積極參加社交活動**：擴展人際圈，增加遇見理想伴侶的機會。無論是參加聚會、興趣班，還是社區活動，這些都是結識新朋友的好方法。

2. **保持開放心態**：對新的關係保持開放和積極的態度，不要因為過去的經歷而封閉自己。`;

  const processedHtml = processMarkdown(testMarkdown);

  return (
    <Box sx={{ 
      p: 4, 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      minHeight: '100vh'
    }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ color: 'white' }}>
          簡單 Markdown 測試
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
        border: '1px solid rgba(255, 255, 255, 0.2)',
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
        '& .md-ol': {
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
        <div dangerouslySetInnerHTML={{ __html: processedHtml }} />
      </Box>
      
      <Box sx={{ mt: 3, p: 2, background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
        <Typography variant="h6" sx={{ color: 'white', mb: 1 }}>
          原始 Markdown:
        </Typography>
        <Typography variant="body2" sx={{ 
          color: 'rgba(255,255,255,0.7)', 
          fontFamily: 'monospace',
          whiteSpace: 'pre-wrap',
          fontSize: '0.9rem'
        }}>
          {testMarkdown}
        </Typography>
      </Box>
    </Box>
  );
};

export default SimpleMarkdownTest;
