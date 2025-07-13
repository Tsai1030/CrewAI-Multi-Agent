import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// 組件導入
import ZiweiForm from './components/ZiweiForm';
import ResultDisplay from './components/ResultDisplaySimple';
import LoadingAnimation from './components/LoadingAnimation';
import WizardDivination from './components/WizardDivination';
import Header from './components/Header';
import SimpleBackground from './components/SimpleBackground';

// 樣式導入
import './App.css';

// 主題配置
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#667eea',
      light: '#8fa4f3',
      dark: '#4c63d2',
    },
    secondary: {
      main: '#764ba2',
      light: '#9575cd',
      dark: '#512da8',
    },
    background: {
      default: 'transparent',
      paper: 'rgba(255, 255, 255, 0.1)',
    },
    text: {
      primary: '#ffffff',
      secondary: 'rgba(255, 255, 255, 0.7)',
    },
  },
  typography: {
    fontFamily: '"Noto Sans TC", "Cinzel", sans-serif',
    h1: {
      fontFamily: '"Cinzel", serif',
      fontWeight: 600,
    },
    h2: {
      fontFamily: '"Cinzel", serif',
      fontWeight: 500,
    },
    h3: {
      fontFamily: '"Cinzel", serif',
      fontWeight: 500,
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '25px',
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
  },
});

function App() {
  const [currentStep, setCurrentStep] = useState('form'); // 'form', 'loading', 'result'
  const [analysisResult, setAnalysisResult] = useState(null);

  const [selectedDomain, setSelectedDomain] = useState(null);
  const [useWizardAnimation, setUseWizardAnimation] = useState(true); // 控制使用哪種載入動畫

  // 處理表單提交
  const handleFormSubmit = async (formData, domain) => {
    setCurrentStep('loading');
    setSelectedDomain(domain);

    try {
      // 調用 API
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          birth_data: formData,
          domain_type: domain.id,
          output_format: 'json_to_narrative',
          show_agent_process: false,
        }),
      });

      const result = await response.json();

      if (result.success) {
        setAnalysisResult(result);
        setCurrentStep('result');
      } else {
        throw new Error(result.error || '分析失敗');
      }
    } catch (error) {
      console.error('分析錯誤:', error);
      // 這裡可以顯示錯誤訊息
      setCurrentStep('form');
    }
  };

  // 重新開始
  const handleRestart = () => {
    setCurrentStep('form');
    setAnalysisResult(null);
    setSelectedDomain(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="App">
        <SimpleBackground />
        <Header />

        <main className="main-content">
          {currentStep === 'form' && (
            <ZiweiForm
              onSubmit={handleFormSubmit}
              useWizardAnimation={useWizardAnimation}
              setUseWizardAnimation={setUseWizardAnimation}
            />
          )}

          {currentStep === 'loading' && (
            useWizardAnimation ? (
              <WizardDivination domain={selectedDomain} />
            ) : (
              <LoadingAnimation domain={selectedDomain} />
            )
          )}

          {currentStep === 'result' && (
            <ResultDisplay
              result={analysisResult}
              domain={selectedDomain}
              onRestart={handleRestart}
            />
          )}
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App;
